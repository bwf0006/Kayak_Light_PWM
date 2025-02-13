import machine
import time
import dht

# Pin configuration
dht_pin = machine.Pin(16)  # Change this to the pin you're using for the DHT22

# Create the DHT22 sensor object
sensor = dht.DHT22(dht_pin)

def read_dht22():
    try:
        # Attempt to read the sensor
        sensor.measure()  # Trigger the measurement
        temp_celsius = sensor.temperature()  # Get temperature in Celsius
        humidity = sensor.humidity()  # Get humidity in percentage
        
        # Convert temperature to Fahrenheit
        temp_fahrenheit = (temp_celsius * 9/5) + 32
        
        # Print temperature in Fahrenheit and humidity
        print(f"Temperature: {temp_fahrenheit:.2f}°F")
        print(f"Humidity: {humidity}%")
    except OSError as e:
        print("Failed to read sensor data:", e)

# Main loop to keep reading data
#while True:
    #read_dht22()
    #time.sleep(2)  # Wait 2 seconds between readings
