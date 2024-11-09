# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    LED CONTROLLER                           CREATED: 2024-10-17          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Basic utility helper to handle the updates to led strips. It utilizes the 'multiprocessing' module to utilize 
#   multiple CPU cores. This allows one core of the system to solely be dedicated to updating the LED's while the main
#   thread can worry about calculating the next values needed to be displayed. 
#
# It also implements a backlog queue of values to be written to the strip. This way the thread responsible for
#   computing the next 'frame' can work ahead a little bit. This allows for frequent hits to performance on not only
#   the system as a whole, but more importantly the thread calculating our next 'frame'. Let's say every 10s the 
#   feature we are running needs 1 full second of processing time. Without a backlog frame queue we would simply have
#   no data for that 1s. Now it can take that performance hit and show no sign to the user assuming under "normal"
#   operation the calcuation is faster than our 'refresh_rate_hz'.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import logging
import multiprocessing
import numpy as np
import time
from rpi_ws281x import PixelStrip, Color

from helpers.decorators import *
from helpers.Settings import Settings

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Basic multithreaded LED controller.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LEDController(LogAllMethods):
    def __init__(self, refresh_rate_hz: int=30, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger()
        self.refresh_rate_hz = refresh_rate_hz
        self.refresh_interval = 1.0 / self.refresh_rate_hz
        
        self.strip = PixelStrip(Settings.NUM_LEDS, Settings.LED_PIN, Settings.LED_FREQ_HZ, Settings.LED_DMA
                                , Settings.LED_INVERT, Settings.LED_BRIGHTNESS, Settings.LED_CHANNEL)
        self.strip.begin()
        
        self.update_queue = multiprocessing.Queue(maxsize=Settings.UPDATE_QUEUE_SIZE)
        self.led_update_process = multiprocessing.Process(target=self._write_queue_to_leds_process, daemon=True)
        self.running = multiprocessing.Value('b', True)
        
        self.led_update_process.start()
        self.update_queue.cancel_join_thread()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running.value = False
        self.led_update_process.join()
        
        # If you don't empty queues they won't "stop" even when you close them.
        while not self.update_queue.empty():
            self.update_queue.get()
        self.update_queue.close()
        self.update_queue.join_thread()

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Process function that takes our 'update_queue' and writes it to our led strip. If we want to end this
                 process you need to set self.running.value to 'False'.
    INPUT: NA
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def _write_queue_to_leds_process(self) -> None:
        while self.running.value:
            start_time = time.time()
            data = self.update_queue.get()
            
            for idx in range(Settings.NUM_LEDS):
                if idx in Settings.BAD_LEDS:
                    color = Color(0, 0, 0)
                else:
                    # Assumes color order is (R, G, B). Need to cast to ints from uint8.
                    color = Color(int(data[idx, 0]), int(data[idx, 1]), int(data[idx, 2]))
                
                self.strip.setPixelColor(idx, color)
            
            self.strip.show()
            elapsed_time = time.time() - start_time
            if elapsed_time > self.refresh_interval:
                self.logger.warning(f"Update took too long. Frame dropped. {elapsed_time:.2f}s")
            
            # Wait for the remaining time to maintain the refresh rate
            time_to_wait = self.refresh_interval - elapsed_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: Puts our 'led_array' onto our 'update_queue' and then checks to see if we should wait before 
                 returning to prevent the caller to overwhelm the controller.
    INPUT: led_array - List of values for our led strip that we will queue to be updated.
    OUTPUT: NA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def update_leds(self, led_array: np.ndarray) -> None:
        # Ensure led_array is a NumPy array of the correct dtype
        assert isinstance(led_array, np.ndarray) and led_array.dtype == np.uint8

        # Check if led_array is a batch of frames or a single frame
        if led_array.ndim == 2:  # Single frame, shape should be (NUM_LEDS, 3)
            self.update_queue.put(led_array)
        elif led_array.ndim == 3:  # Multiple frames, shape should be (num_frames, NUM_LEDS, 3)
            for frame in led_array:
                self.update_queue.put(frame)
        else:
            raise ValueError("led_array must be a 2D or 3D array representing RGB frames.")

# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════