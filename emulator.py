import paho.mqtt.client as mqtt
import random
import time

# MQTT Broker
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DHT = "greenhouse/sensors/dht"

# Simulate the DHT sensor (temperature & humidity)
def emulate_dht_sensor(client):
    temperature = 20 + random.uniform(-2, 5)  # Simulated temperature
    humidity = 60 + random.uniform(-10, 10)   # Simulated humidity
    dht_data = f"Temperature: {temperature:.2f}C, Humidity: {humidity:.2f}%"
    client.publish(TOPIC_DHT, dht_data)
    print(f"Published DHT Sensor Data: {dht_data}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print(f"Failed to connect, return code {rc}")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Greenhouse_Emulator")
    client.on_connect = on_connect

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    while True:
        emulate_dht_sensor(client)
        time.sleep(5)  # Delay between readings

if __name__ == "__main__":
    main()
