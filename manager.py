import paho.mqtt.client as mqtt

# MQTT Broker
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DHT = "greenhouse/sensors/dht"
TOPIC_BUTTON = "greenhouse/button"
TOPIC_RELAY = "greenhouse/relay"

IRRIGATION_THRESHOLD = 22.0  # Temperature threshold for activating irrigation
HUMIDITY_THRESHOLD = 65.0    # Humidity threshold above which irrigation is unnecessary

# MQTT Callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(TOPIC_DHT)
        client.subscribe(TOPIC_BUTTON)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_DHT:
        handle_dht_data(msg.payload.decode(), client)
    elif msg.topic == TOPIC_BUTTON:
        handle_button_action(msg.payload.decode(), client)

# Handle DHT data (temperature & humidity)
def handle_dht_data(data, client):
    print(f"Received DHT data: {data}")
    temperature = float(data.split(",")[0].split(":")[1].strip().replace("C", ""))
    humidity = float(data.split(",")[1].split(":")[1].strip().replace("%", ""))
    
    print(f"Extracted Temperature: {temperature}")
    print(f"Extracted Humidity: {humidity}")

    # Turn on irrigation system if temperature is above the threshold and humidity is below 65%
    if temperature > IRRIGATION_THRESHOLD and humidity < HUMIDITY_THRESHOLD:
        print("Temperature is high and humidity is low. Activating irrigation system...")
        client.publish(TOPIC_RELAY, "ON")
    else:
        print("Conditions not met for irrigation. Deactivating irrigation system...")
        client.publish(TOPIC_RELAY, "OFF")

# Handle manual button action (manual override for relay)
def handle_button_action(action, client):
    print(f"Button manually set to: {action}")

    if action == "ON":
        client.publish(TOPIC_RELAY, "ON")  # Manual override turns on irrigation
        print("Manual override: Irrigation system turned ON by the button.")
    elif action == "OFF":
        client.publish(TOPIC_RELAY, "OFF")  # Manual override turns off irrigation
        print("Manual override: Irrigation system turned OFF by the button.")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Greenhouse_Manager")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
