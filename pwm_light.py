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
- Controls PWM and three override switches, set invert = 1 or 0 depending on circuit, adjust threshold values for override brightness settings
    adjust increment for higher or lower incrementing of brightness, adjust hold_threshold for duration required to register button hold,
    only: start_pwm_light() is needed to call, initialize, and attach interrupts

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
# Invert pwm logic? for inverted duty cycle: 1=invert 0=regular
invert = 1

# Constants for brightness levels
high_thresh = 63000 #high bright, max thresh = 65535
mid_thresh = 10000
low_thresh = 1000 #low bright, min thresh = 1 since 0 reserved for off
increment = 1000

hold_threshold = 0.8  # seconds

# PWM setup
pwm = PWM(Pin(6))
pwm.freq(1000)  #1kHz freq
x = 32767  #Initial brightness set point
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
    if invert == 1:
        x_actual = abs(x-65535)
    else:
        x_actual = x
    pwm.duty_u16(x_actual)    
    display_brightness()
    
'''-------------------------Display Brightness--------------------------------'''
# Display brightness in percent or high/low/off
def display_brightness():
    global invert
    if x == high_thresh:
        tm1637_custom.show_bright_percentage(0,"high ")
    elif x == low_thresh:
        tm1637_custom.show_bright_percentage(0,"low ")
    elif x == 0:
        tm1637_custom.show_bright_percentage(0,"off ")
    else:
        tm1637_custom.show_bright_percentage(1,x) #calculates percent doesnt need inversion

'''------------------------------SW Hold--------------------------------------'''
# Brightness control functions
def top_hold():
    global x
    if x != 0: #if not off   
        x = high_thresh
        set_x(x)

def middle_hold():
    global x
    if x != 0:
        x = mid_thresh
        set_x(x)

def bottom_hold():
    global x
    if x != 0:
        x = low_thresh
        set_x(x)

'''------------------------------SW Press-------------------------------------'''
def top_press():
    global x, increment
    if x != 0:
        if x < high_thresh - increment:
            x += increment
        else:
            x = high_thresh
        set_x(x)

def middle_press():
    global x
    global last_valid_x
    # Toggle between 0 and the last valid x value
    if x != 0:
        last_valid_x = x #saves value if not off
    if x == 0:       #if off, sets x to last valid x
        x = last_valid_x
    else:
        x = 0
    set_x(x)

def bottom_press():
    global x, increment
    if x != 0:    
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
        time.sleep_ms(debounce_delay)  #short debounce
        if top_sw.value() == 0:  #check if still pressed
            press_time = time.ticks_ms() #start counting time
            while top_sw.value() == 0:
                time.sleep(0.01) #more delay
                if time.ticks_diff(time.ticks_ms(), press_time) > hold_threshold * 1000: #if held
                    #print("Top switch is held") #debug statement
                    top_hold()
                    break
            else:
                #print("Top switch is pressed") #debug statement
                top_press()
            while top_sw.value() == 0:  #wait for release
                time.sleep(0.01)
            top_sw_last_state = 1  #only update on release
            
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