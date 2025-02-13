'''
Filename: tm1637_custom.py
Author: Brad Farris
Date: 2/12/25
Description: Setup and Custom functions for tm1637 driver
Version: 1.0

Default Pinout:
- GPIO7 -> LED Display CLK
- GPIO8 -> LED Display DIO
- Display Vcc -> 3.3v
- Display gnd -> gnd

Dependencies:
- tm1637

Usage:
- load(state)
    state=1 -> start loading graphic
    state=0 -> stop loading graphic
- show_brightness_percentage(is_num, value, duration)
    is_num=1 -> expects numerical value, is_num!=1 -> expects str
    value = actual value passed (numerical value or str)
    duration = time in ms
- custom_scroll(message, duration)
    just calls tm.scroll() and passes same info

Notes:
- change custom_scroll in main to just call tm.scroll, must import from tm1637 there then get rid of custom_scroll
- display sometimes doesn't show long enough, timing issues to sort out
'''

'''----------------------------imports----------------------------------------'''
import time
import machine
import tm1637
from machine import Pin
from machine import Timer

'''------------------------------Setup----------------------------------------'''
tm = tm1637.TM1637(clk=Pin(7), dio=Pin(8))
load_timer = machine.Timer()  # Define globally

'''------------------------------Load-----------------------------------------'''
def load(state):
    global load_timer  # Reference the global timer
    if state == 1:
        pattern = [0b00000001, 0b00000010, 0b00000100, 0b00001000,  
                   0b00010000, 0b00100000, 0b01000000, 0b10000000]
        tm.write([0, 0, 0, 0])  # Clear the display first
        index = 0  # Tracks current pattern position
        def update_display(timer):
            nonlocal index  # Allow modification of the index variable
            data = [pattern[index], pattern[index] & 0b01111111, pattern[index], pattern[index]]  # Ensure colon is off
            tm.write(data)  
            index = (index + 1) % len(pattern)  # Loop through the pattern
        load_timer.init(period=100, mode=machine.Timer.PERIODIC, callback=update_display)
    else:
        load_timer.deinit()  # Stop the timer if load(0) is called

'''--------------------------Show Brightness %--------------------------------'''
def show_bright_percentage(is_num, value, duration=2000):  # duration in milliseconds
    tm.show("")
    if is_num == 0: #display high/off/low if at those values
        tm.show(value)
    else: #display percentage based on inverted pwming from 0-65535
        value = int(65536 - (value/65636)*100) #calculate brightness
        percent_1 = 0b01100011  # Third digit |-- %   |
        percent_2 = 0b01011100  # Fourth digit|     --|
        tens = value // 10  # Extract tens place
        ones = value % 10   # Extract ones place
        tm.write([tm.encode_digit(tens), tm.encode_digit(ones), percent_1, percent_2])
    # Create a timer
    clear_timer = Timer(-1)  # Local timer instance
    # Start a one-time timer to clear the display after `duration` ms
    clear_timer.init(mode=Timer.ONE_SHOT, period=duration, callback=lambda t: tm.show("    "))

'''------------------------------Scroll---------------------------------------'''
def custom_scroll(message,duration):
    tm.scroll(message,duration)