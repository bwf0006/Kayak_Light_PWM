'''
Filename: ir_remote.py
Author: Brad Farris
Date: 2/12/25
Description: IR remote program for PWM kayak light
Version: 1.0

Default Pinout:
- GPIO17 -> ir sensor data
- sensor vcc -> 3.3v
- sensor gnd -> gnd

Dependencies:
- tm1637

Usage:
- press_button_action_X() *where X = button label on remote
    description here
- held_button_action_X() *where X = button label on remote
    description here

Notes:
- change array level[] values to practical #'s through testing
'''

'''----------------------------imports----------------------------------------'''
from machine import Pin
import time
import pwm_light
from ir_rx.nec import NEC_8
from ir_rx.print_error import print_error

'''------------------------------Setup----------------------------------------'''
ir_pin = Pin(17, Pin.IN)
repeat = 0
last_data = 0
level = [5000, 10000, 15000, 25000, 33000, 45000, 55000] #array of brightness values assigned to buttons 2-8, 1 and 9 reserved

'''--------------------------Button actions-----------------------------------'''
# all unused contain pass, mapped for future modifications
# Button '1' action
def press_button_action_1():
    #print("button '1' pressed") #debug statement
    pwm_light.bottom_hold()
    
def held_button_action_1():
    #print("button '1' held") #debug statement
    pass

# Button '2' action
def press_button_action_2():
    #print("button '2' pressed") #debug statement
    x = pwm_light.x
    if x != 0:
        pwm_light.set_x(level[0])
    
def held_button_action_2():
    #print("button '2' held") #debug statement
    pass

# Button '3' action
def press_button_action_3():
    #print("button '3' pressed") #debug statement
    x = pwm_light.x
    if x != 0:
        pwm_light.set_x(level[1])

def held_button_action_3():
    #print("button '3' held") #debug statement
    pass

# Button '4' action
def press_button_action_4():
    #print("button '4' pressed") #debug statement
    x = pwm_light.x
    if x != 0:
        pwm_light.set_x(level[2])
    
def held_button_action_4():
    #print("button '4' held") #debug statement
    pass

# Button '5' action
def press_button_action_5():
    #print("button '5' pressed") #debug statement
    x = pwm_light.x
    if x != 0:
        pwm_light.set_x(level[3])
    
def held_button_action_5():
    #print("button '5' held") #debug statement
    pass

# Button '6' action
def press_button_action_6():
    #print("button '6' pressed") #debug statement
    x = pwm_light.x
    if x != 0:
        pwm_light.set_x(level[4])
    
def held_button_action_6():
    #print("button '6' held") #debug statement
    pass

# Button '7' action
def press_button_action_7():
    #print("button '7' pressed") #debug statement
    x = pwm_light.x
    if x != 0:
        pwm_light.set_x(level[5])
    
def held_button_action_7():
    #print("button '7' held") #debug statement
    pass

# Button '8' action
def press_button_action_8():
    #print("button '8' pressed") #debug statement
    x = pwm_light.x
    if x != 0:
        pwm_light.set_x(level[6])
    
def held_button_action_8():
    #print("button '8' held") #debug statement
    pass

# Button '9' action
def press_button_action_9():
    #print("button '9' press") #debug statement
    pwm_light.top_hold()
    
def held_button_action_9():
    #print("button '9' held") #debug statement
    pass
    
# Button '*' action
def press_button_action_star():
    #print("button '*' pressed") #debug statement
    pwm_light.middle_press()
    
def held_button_action_star():
    #print("button '*' held") #debug statement
    pass

# Button '0' action
def press_button_action_0():
    #print("button '0' pressed") #debug statement
    pass

def held_button_action_0():
    #print("button '0' held") #debug statement
    pass

# Button '#' action
def press_button_action_pound():
    #print("button '#' pressed") #debug statement
    pass

def held_button_action_pound():
    #print("button '#' held") #debug statement
    pass

# Button 'Up' action
def press_button_action_up():
    #print("button 'Up' pressed") #debug statement
    pwm_light.top_press()
          
def held_button_action_up():
    #print("button 'Up' held") #debug statement
    pwm_light.top_press()

# Button 'Down' action
def press_button_action_down():
    #print("button 'Down' pressed") #debug statement
    pwm_light.bottom_press()

def held_button_action_down():
    #print("button 'Down' held") #debug statement
    pwm_light.bottom_press()

# Button 'Left' action
def press_button_action_left():
    #print("button 'Left' pressed") #debug statement
    pass

def held_button_action_left():
    #print("button 'Left' held") #debug statement
    pass

# Button 'Right' action
def press_button_action_right():
   #print("button 'Right' pressed") #debug statement
    pass

def held_button_action_right():
    #print("button 'Right' held") #debug statement
    pass

# Button 'OK' action
def press_button_action_ok():
    #print("button 'OK' pressed") #debug statement
    pass

def held_button_action_ok():
    #print("button 'OK' held") #debug statement
    pass

'''---------------------------Data Dictionary---------------------------------'''
#dictionary mapping button codes to actions for press and holds
button_actions = {
    #Button '1'
    0x45: (press_button_action_1, held_button_action_1),
    #Button '2'
    0x46: (press_button_action_2, held_button_action_2),
    #Button '3'
    0x47: (press_button_action_3, held_button_action_3),
    #Button '4'
    0x44: (press_button_action_4, held_button_action_4),
    #Button '5'
    0x40: (press_button_action_5, held_button_action_5),
    #Button '6'
    0x43: (press_button_action_6, held_button_action_6),
    #Button '7'
    0x07: (press_button_action_7, held_button_action_7),
    #Button '8'
    0x15: (press_button_action_8, held_button_action_8),
    #Button '9'
    0x09: (press_button_action_9, held_button_action_9),
    #Button '*'
    0x16: (press_button_action_star, held_button_action_star),
    #Button '0'
    0x19: (press_button_action_0, held_button_action_0),
    #Button '#'
    0x0d: (press_button_action_pound, held_button_action_pound),
    #Button 'Up'
    0x18: (press_button_action_up, held_button_action_up),
    #Button 'Down'
    0x52: (press_button_action_down, held_button_action_down),
    #Button 'Left'
    0x08: (press_button_action_left, held_button_action_left),
    #Button 'Right'
    0x5a: (press_button_action_right, held_button_action_right),
    #Button 'OK'
    0x1c: (press_button_action_ok, held_button_action_ok)
}

'''---------------------------Handle Buttons----------------------------------'''
def handle_button(button, action_type):
    #check if the button code is in the dictionary
    if button in button_actions:
        # Get the tuple (press_action, hold_action)
        press_action, hold_action = button_actions[button]
        
        # Call the correct action based on action_type
        if action_type == 0:  # 0 means press
            press_action()
        elif action_type == 1:  # 1 means held
            hold_action()
    else:
        print(f"Error: Button {button} not mapped")        

'''------------------------Receive/Handle data--------------------------------'''
# Callback function that is called when data is received from the IR receiver
def cb(data, addr, ctrl):
    global repeat
    global last_data
    button = None
    
    # Repeat Press but 'debounced'
    if data < 0 and repeat <= 1:
        repeat += 1
        #print("Repeat code.") #debuggin statement
        
    # Repeat Press over threshold = Held down
    elif data < 0 and repeat > 1:
        repeat += 1
        #hex_value = f"0x{last_data:02x}" #debug statement
        button = last_data
        #print(f"Held: {hex_value}") #debuggin statement
        #held_button(button)
        handle_button(button, 1)  # 1 for Held action
    
    # Button Press
    else:
        #print(f"Received data: 0x{data:02x}") #debuggin statement
        repeat = 0
        last_data = data
        button = data
        #print(f"Last data: 0x{data:02x}") #debuggin statement
        #press_button(button)
        handle_button(button, 0)  # 0 for Press action

'''------------------------------Startup--------------------------------------'''
def start_ir_receiver():

    # Create the IR receiver instance using NEC 8-bit protocol
    ir_receiver = NEC_8(ir_pin, cb)

    # Error handling
    ir_receiver.error_function(print_error)

    #print("Ir Remote initialized") #debug statement

    return ir_receiver