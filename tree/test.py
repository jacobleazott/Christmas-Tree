# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                             ╠══╣
# ║  ║    LED CONTROLLER                           CREATED: 2024-10-17          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                             ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ════════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# Basic utility helper to handle the updates to led strips using the neopixel library.
# 
# I think the main idea is to handle our threading for updating the pixels, and handling any color format that we
#   could think to pass in. On top of that enabling things like gamma correction or other fun things like that.
# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import logging
import multiprocessing
import os
import signal
import sys
import time
from rpi_ws281x import PixelStrip, Color

from decorators import *
from Settings import Settings

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class LEDController(LogAllMethods):
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

        signal.signal(signal.SIGINT, self.handle_signal)
        
    def __enter__(self):
        self.running.value = True
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def handle_signal(self, signum, frame):
        self.logger.info(f"Signal received: {signum}, terminating LED controller...")
        self.stop()
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def start(self):
        if self.led_update_process is None:
            self.led_update_process = multiprocessing.Process(target=self.write_queue_to_leds)
            self.led_update_process.start()
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def stop(self):
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
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def update_pixels(self, pixel_array: list) -> None:
        for idx, pixel_val in enumerate(pixel_array):
            color = Color(*pixel_val)  # Assuming pixel_val is (R, G, B)
            self.strip.setPixelColor(idx, color)
        self.strip.show()

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def write_queue_to_leds(self):
        while self.running.value:
            try:
                # Try to get an update from the queue
                pixel_array = self.update_queue.get(timeout=self.refresh_interval)
                start_time = time.time()
                self.update_pixels(pixel_array)
                elapsed_time = time.time() - start_time

                # Check Timing
                if elapsed_time > self.refresh_interval:
                    self.logger.warning(f"Update took too long. Frame dropped. {elapsed_time} {self.refresh_interval}")

                # Wait for the remaining time to maintain the refresh rate
                time_to_wait = self.refresh_interval - elapsed_time
                if time_to_wait > 0:
                    time.sleep(time_to_wait)

            except queue.Empty:
                # If no updates are in the queue, just wait for a while
                time.sleep(self.refresh_interval)

    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def wait_for_queue_size(self):
        while True:
            current_size = self.update_queue.qsize()
            if current_size < Settings.UPDATE_QUEUE_SIZE:
                return
            else:
                self.logger.debug(f"Current queue size is {current_size}. Waiting...") 
                time.sleep(self.refresh_interval)  # Wait before checking again
    
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    DESCRIPTION: 
    INPUT: 
    OUTPUT: 
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""''"""
    def update_leds(self, pixel_array):
        self.update_queue.put(pixel_array)
        self.wait_for_queue_size()

# FIN ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════