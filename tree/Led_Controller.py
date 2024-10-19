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
import os
import signal
import sys
import time
from rpi_ws281x import PixelStrip, Color
import queue

from decorators import *
from Settings import Settings

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Basic multithreaded LED controller.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LEDController():
    def __init__(self, refresh_rate_hz=30, logger: logging.Logger=None):
        self.logger = logger if logger is not None else logging.getLogger()
        
        self.strip = PixelStrip(Settings.NUM_LEDS, Settings.LED_PIN, Settings.LED_FREQ_HZ, Settings.LED_DMA
                                , Settings.LED_INVERT, Settings.LED_BRIGHTNESS, Settings.LED_CHANNEL)
        self.strip.begin()
        
        self.update_queue = multiprocessing.Queue(maxsize=Settings.UPDATE_QUEUE_SIZE)
        self.led_update_process = None
        self.running = multiprocessing.Value('b', False)

        self.refresh_rate_hz = refresh_rate_hz
        self.refresh_interval = 1.0 / self.refresh_rate_hz
        
    def __enter__(self):
        self.running.value = True
        if self.led_update_process is None:
            self.led_update_process = multiprocessing.Process(target=self._write_queue_to_leds_process)
            self.led_update_process.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running.value = False
        if self.led_update_process is not None:
            self.led_update_process.join()
            self.led_update_process = None
        
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
        count = 0
        while self.running.value:
            start_time = time.time()
            data = self.update_queue.get()
            
            for idx in range(Settings.NUM_LEDS):
                color = Color(*data[idx])  # Assuming pixel_val is (R, G, B)
                self.strip.setPixelColor(idx, color)
            self.strip.show()

            count += 1
            print("Hows the COunt?", count, data[Settings.NUM_LEDS+1])
            
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
    def update_leds(self, led_array: list) -> None:
        self.update_queue.put(led_array)
        # x = 100
        # print(sys.getsizeof(x))
        # print(sys.getsizeof(led_array))
        # print("Added element", led_array[Settings.NUM_LEDS+1], self.update_queue.qsize())
        

# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════