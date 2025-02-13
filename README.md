# Kayak Light PWM

## Features

### Current Features:
1. Controlled by Raspberry Pi Pico 2
2. Adjustable brightness for Harbor Freight Roadshock 3in LED flood light
3. Board mounted override brightness setting buttons
4. Temp/Humidity interface

### Temporary Features:
1. IR remote controlled brightness settings - replace with bluetooth or RF control

### Planned Features:
1. Bluetooth or RF brightness control settings controlled through DIY remote
2. Temp/Humidity logging
3. GPS/NAV data logging
4. Battery capacity estimator with low voltage shutoff

## Using AI for battery capacity estimation

### Gather Data
Use the RP Pico, INA260, and SD Card module to vary load and collect: 
timestamp, current, batt_voltage, resting_batt_voltage (turn off load, delay, read V), est. capacity (map to battery capacity chart)

### Process Data
1. Keep current, batt_voltage, est. capacity
2. Feed this data to polynomial regression AI model

### Impliment 
1. Implement resulting formula on pico and test
2. revamp if necessary
3. ???
4. profit

## Create auto shutoff
Set est. capcity = estimated resting voltage auto shutoff function

## Code Explanations

### Code 1 Explained here:

- 1
- 2
- 3
- ...

## Notes:

### Light Notes:
[Roadshock LED Flood](https://www.harborfreight.com/3-in-led-flood-light-64322.html)
* Light is a harbor freight ROADSHOCK 3 in. LED Flood Light
    Must open up case and solder wire to PWM dimming inputs on each TP8005s then these tie together
    Must also run this dimming wire externally (drill hole and epoxy wire in to maintain waterproofing)
* Chips on Flood light we are interfacing are TP8005.
* Datasheet TP8005_translated.pdf is translated by google translate, it is mostly readable.
* The TP8005 pwm pins are pulled up to 5v internally by default which is why we short it to ground with a ZVN211A N channel mosfet. We
  drive its gate with our PWM signal so the duty cycle is inverted.
* This dimming PWM pin can be driven directly with 5v PWM from something like an arduino, but use caution as it will draw a lot of current if
  driven when power is disconnected from the 12-24v input of the light. It's safer to use a mosfet to drive it.

### ZVN2110A MOSFET
Overkill but its what I have on hand
Vgs_thresh: min = .8v, max = 2.4v
Rds_on = 4ohm at Vgs = 10v and Id = 1A  
  *likely much higher at 3.3v especially in when not in saturation but this is acceptable for this application

### Pico Notes:
* RP Pico 2
* Power VSYS with 5v input from 7805 regulator
* Power all components with picos 3.3v supply
* Pins ARE NOT 5v tolerant
* Include reset? if so include button to short RUN pin
* GPIO26-29 are ADC inputs and easy to fry, make absolutely sure that input wont exceed VDDIO + ~300mv, i.e. do not apply input to these pins when pico is off

### IR Remote
[Infrared IR Wireless Remote Control Module Kits DIY Kit HX1838](https://www.amazon.com/dp/B09ZTZQFP7?ref=ppx_yo2ov_dt_b_fed_asin_title)

### GPS Module
[GPS Module,Navigation Satellite Positioning NEO-6M, GT-07](https://www.amazon.com/dp/B0B31NRSD2?ref=ppx_yo2ov_dt_b_fed_asin_title)
* Vcc requires 5v - it feeds an onboard 5 to 3.3v regulator, tested and works with 3.3v input but for longevity should use 5v
* Feed Vcc with the 7805
* Tx and Rx 3.3v so safe for pico

### SD Card Module
[Micro SD Card Module TF Card Memory Storage Adapter Reader Board SPI Interface with Integrated Circuit Breakout](https://www.amazon.com/dp/B08C4WY2WR?ref=ppx_yo2ov_dt_b_fed_asin_title)

### LED display
[4 Digit 7 Segment Digital Tube LED Display Board](https://www.amazon.com/dp/B0BFQNFX6D?ref=ppx_yo2ov_dt_b_fed_asin_title)
* Layout: 88:88

### ADAFRUIT 4226
Breakout board for INA260
[Digikey Adafruit 4226](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4226/10130492)
* Need to adapt to micropython
* Received broken component - get another
