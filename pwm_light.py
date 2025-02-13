'''
Filename: pwm_light.py
Author: Brad Farris
Date: 2/12/25
Description: PWM and override switch control for Kayak light
Version: 1.0

Default Pinout:
- GPIO20 -> top_sw
- GPIO21 -> middle_sw
- GPIO22 -> bottom_sw
- GPIO6(pwm) -> to gate of mosfet
- other pin of each sw to gnd, no external pull resistors required

Dependencies:
- tm1637_custom
- tm1637

Usage:
- Explain how to run the script, including any command-line arguments if applicable.

Notes:
- interrupts for the three buttons (top_sw, middle_sw, bottom_sw)
'''

'''----------------------------imports----------------------------------------'''
import machine
import time
from machine import Pin, PWM
import tm1637
import tm1637_custom

'''------------------------------Setup----------------------------------------'''
# Constants for brightness levels *PWM duty cycle inverted now with mosfet driving
high_thresh = 63000 #high bright
mid_thresh = 10000
low_thresh = 1000 #low bright
increment = 1000

hold_threshold = 0.8  # seconds

# PWM setup
pwm = PWM(Pin(6))
pwm.freq(1000)  # 1 kHz frequency
x = 32767  # Initial brightness set point #duty cycle with max of 65535
pwm.duty_u16(x)

# Switches setup
top_sw = Pin(20, Pin.IN, Pin.PULL_UP)
middle_sw = Pin(21, Pin.IN, Pin.PULL_UP)
bottom_sw = Pin(22, Pin.IN, Pin.PULL_UP)

top_sw_last_state = 1
middle_sw_last_state = 1
bottom_sw_last_state = 1

'''------------------------------Set PWM--------------------------------------'''
def set_x(val):
    global x
    x = val
    pwm.duty_u16(x)
    display_brightness()
    
'''-------------------------Display Brightness--------------------------------'''
# Display brightness when controlled by switches, not ir remote
def display_brightness():
    if x == high_thresh:
        tm1637_custom.show_bright_percentage(0,"low ")#led at low, mosfet driven low duty cycle -> light high
    elif x == low_thresh:
        tm1637_custom.show_bright_percentage(0,"high")#led at bright, mosfet driven high duty cycle -> light low
    elif x==65535:
        tm1637_custom.show_bright_percentage(0,"off ")#led will be at brightest, mosfet driven 100percent
    else:
        tm1637_custom.show_bright_percentage(1,x)

'''------------------------------SW Hold--------------------------------------'''
# Brightness control functions
def bottom_hold():
    global x
    if x != 65535: #if not off   
        x = high_thresh
        set_x(x)

def middle_hold():
    global x
    if x != 0:
        x = mid_thresh
        set_x(x)

def top_hold():
    global x
    if x != 65535:
        x = low_thresh
        set_x(x)

'''------------------------------SW Press-------------------------------------'''
def bottom_press():
    global x, increment
    if x != 65535:
        if x < high_thresh - increment:
            x += increment
        else:
            x = high_thresh
        set_x(x)

def middle_press():
    global x
    global last_valid_x
    # Toggle between 0 and the last valid x value
    if x != 65535:
        last_valid_x = x #saves value if not off
    if x == 65535:       #if off, sets x to last valid x
        x = last_valid_x
    else:
        x = 65535 #led high but mosfet gate on full -> light off
    set_x(x)

def top_press():
    global x, increment
    if x != 65535:    
        if x > increment + low_thresh:
            x -= increment
        else:
            x = low_thresh
        set_x(x)

'''-----------------------------Interrupts------------------------------------'''
# Interrupt handler function that checks for presses or holds
def check_switch_state():
    global top_sw_last_state, middle_sw_last_state, bottom_sw_last_state
    debounce_delay = 50  # Debounce time in milliseconds (adjust if needed)
    
    if top_sw.value() == 0 and top_sw_last_state == 1:
        time.sleep_ms(debounce_delay)  # Short debounce delay
        if top_sw.value() == 0:  # Confirm it's still pressed
            press_time = time.ticks_ms()
            while top_sw.value() == 0:
                time.sleep(0.01)
                if time.ticks_diff(time.ticks_ms(), press_time) > hold_threshold * 1000:
                    #print("Top switch is held") #debug statement
                    top_hold()
                    break
            else:
                #print("Top switch is pressed") #debug statement
                top_press()
            while top_sw.value() == 0:  # Wait for release
                time.sleep(0.01)
            top_sw_last_state = 1  # Only update once released
            
    if middle_sw.value() == 0 and middle_sw_last_state == 1:
        time.sleep_ms(debounce_delay)
        if middle_sw.value() == 0:
            press_time = time.ticks_ms()
            while middle_sw.value() == 0:
                time.sleep(0.01)
                if time.ticks_diff(time.ticks_ms(), press_time) > hold_threshold * 1000:
                    #print("Middle switch is held") #debug statement
                    middle_hold()
                    break
            else:
                #print("Middle switch is pressed") #debug statement
                middle_press()
            while middle_sw.value() == 0:
                time.sleep(0.01)
            middle_sw_last_state = 1  

    if bottom_sw.value() == 0 and bottom_sw_last_state == 1:
        time.sleep_ms(debounce_delay)
        if bottom_sw.value() == 0:
            press_time = time.ticks_ms()
            while bottom_sw.value() == 0:
                time.sleep(0.01)
                if time.ticks_diff(time.ticks_ms(), press_time) > hold_threshold * 1000:
                    #print("Bottom switch is held") #debug statement
                    bottom_hold()
                    break
            else:
                #print("Bottom switch is pressed") #debug statement
                bottom_press()
            while bottom_sw.value() == 0:
                time.sleep(0.01)
            bottom_sw_last_state = 1  

'''------------------------------Startup--------------------------------------'''
# Main setup function
def start_pwm_light():
    # Attach interrupts to switches (falling edge)
    top_sw.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: check_switch_state())
    middle_sw.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: check_switch_state())
    bottom_sw.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: check_switch_state())
    #print("PWM light control initialized.") #debug statement