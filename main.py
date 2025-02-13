'''
Filename: main.py
Author: Brad Farris
Date: 2/12/25
Description: Briefly describe what this script does.
Version: 1.0

Default Pinout:
- GPIOXX -> Component PinXX

Dependencies:
- pwm_light.py
- ir_remote
- dht22
- tm1637
- tm1637_custom

Usage:
- *Light is a harbor freight ROADSHOCK 3 in. LED Flood Light
    Must open up case and solder wire to PWM dimming inputs on each TP8005s then these tie together
    Must also run this dimming wire externally (drill hole and epoxy wire in to maintain waterproofing)
- Currently performs initialization of pwm_light, then ir_remote,
    then starts main loop which reads dht22 and prints temp and humidity

Notes:
- Any additional information or warnings.
- Need to add:
    * P, I, V readings and shutoff for low battery
    * incorperate formula created with AI to estimate battery capacity from I and V while under load
    * GPS
    * use dht22 to aid in calculations for battery capacity
    * update with permanent rf remote (not temp solution: ir remote)
    * implement SD card write for datalogging
'''
import time
import pwm_light #import pwm module: pwm settings for light and override switches
import ir_remote  # Import the IR remote module
import dht22 #import dht22 temp/humidity module
import tm1637
import tm1637_custom

def main():
    tm1637_custom.tm.show("strt") #debug statement
    time.sleep(.5)
    tm1637_custom.custom_scroll("light init",150) #debug statement
    tm1637_custom.load(1)
    time.sleep(1)
    pwm_light.start_pwm_light() #Start PWM and look for sw interrupts
    tm1637_custom.load(0)
    tm1637_custom.custom_scroll("ir init",150) #debug statement
    tm1637_custom.load(1)
    time.sleep(.5)
    ir_remote.start_ir_receiver()  #Start looking for IR remote
    tm1637_custom.load(0)
    tm1637_custom.tm.show("done") #debug statement
    time.sleep(.5)
    tm1637_custom.tm.show("    ")
    
    # Main Loop
    try:
        while True:
            # Perform tasks
            dht22.read_dht22() #get temp/humidity
            time.sleep(2)  #wait 2 seconds between readings
    except KeyboardInterrupt:
        print("Program exited.")

if __name__ == "__main__":
    main()
