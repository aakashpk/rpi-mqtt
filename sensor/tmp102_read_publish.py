import time
import smbus
import json
import argparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from systemd.journal import JournalHandler  # Import for journal logging
import logging

# Argument parsing
parser = argparse.ArgumentParser(description='TMP102 MQTT Sensor Publisher')
parser.add_argument('--broker', required=True, help='MQTT broker IP address')
parser.add_argument('--port', type=int, default=1883, help='MQTT broker port (default: 1883)')
parser.add_argument('--topic', default='sensors/temperature', help='MQTT topic to publish to')
parser.add_argument('--serial_number', default='xxxx', help='unique sensor serial number')
args = parser.parse_args()

# I2C and TMP102 setup
bus = smbus.SMBus(1)
TMP102_ADDRESS = 0x48

# Setup logging to systemd journal
logger = logging.getLogger('tmp102_sensor')
logger.addHandler(JournalHandler())
logger.setLevel(logging.INFO)

def is_tmp102_connected():
    try:
        # Attempt to read a byte from the TMP102 address
        bus.read_byte(TMP102_ADDRESS)
        return True
    except OSError:
        return False

def read_temperature():
    raw = bus.read_word_data(TMP102_ADDRESS, 0)
    raw_swapped = ((raw << 8) & 0xFF00) + (raw >> 8)
    temp_c = (raw_swapped >> 4) * 0.0625
    return temp_c

# MQTT Callbacks
def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.error("Unexpected disconnection from MQTT broker.")
        print("Error: Unexpected disconnection from MQTT broker.")

# MQTT Setup
mqtt_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
mqtt_client.connect(args.broker, args.port, 60)
mqtt_client.loop_start()

if not is_tmp102_connected():
    error_message = "Error: TMP102 sensor not detected. Please check the connection."
    print(error_message)  # Print the error message to the console
    logger.error(error_message)  # Log the error to the journal
    exit(1)

try:
    while True:
        temperature = read_temperature()
        payload = json.dumps({
            "measurement": "temperature",
            "location": "raspberry_pi",
            "sensor_type": "tmp102",
            "unit": "C",
            "serial_number": args.serial_number,
            "fields": {
                "value": temperature
            }
        })
        mqtt_client.publish(args.topic, payload)
        print(f"Published to {args.topic}: {payload}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping...")
    mqtt_client.disconnect()