from machine import Pin, ADC
import dht
import time

# --- Pin Configurations ---
dht_sensor = dht.DHT22(Pin(15)) 
soil_adc = ADC(Pin(26))
pump_relay = Pin(14, Pin.OUT)
status_led = Pin(16, Pin.OUT)

# --- Configuration Constants ---
SOIL_THRESHOLD = 30000
CHECK_INTERVAL = 2

# --- Helper Functions ---
def read_sensors():
    # Read DHT22
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    
    # Read Soil Moisture Sensor (ADC 16-bit reading: 0 - 65535)
    soil_value = soil_adc.read_u16()
    
    return temp, humidity, soil_value

def control_irrigation(soil_val):
    if soil_val < SOIL_THRESHOLD:
        pump_relay.value(1)   # Turn ON pump
        status_led.value(1)   # Alert LED ON
        print("[ACTION] Soil dry. Pump activated.")
    else:
        pump_relay.value(0)   # Turn OFF pump
        status_led.value(0)   # Alert LED OFF
        print("[ACTION] Soil moist. Pump off.")

# --- Main Control Loop ---
pump_relay.value(0)           # Ensure pump is off on boot

while True:
    try:
        temp, humidity, soil = read_sensors()
        print(f"Temp: {temp}°C | Humidity: {humidity}% | Soil ADC: {soil}")
        
        control_irrigation(soil)
        
    except Exception as e:
        print(f"Sensor Error: {e}")
        
    time.sleep(CHECK_INTERVAL)
