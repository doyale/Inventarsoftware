import time
import os

global debug_print, ref_time
debug_print = False # set to true to display debug messages
ref_time = round(time.time() * 1000) #time in micros at program start

def debug(text: str): #debug break points (only if enabled)
    os.system('') # required to show color text correctly
    global debug_print, ref_time
    if debug_print == True:
        current_time = round(time.time() * 1000)
        print(f"Time since last debug call: \033[92m{current_time-ref_time} ms\033[0m, Debug Message: \033[93m{text}\033[0m")
        ref_time = current_time