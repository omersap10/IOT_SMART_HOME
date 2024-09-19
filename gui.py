import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
import paho.mqtt.client as mqtt

# MQTT Broker
BROKER = 'broker.hivemq.com'
PORT = 1883
TOPIC_DHT = "greenhouse/sensors/dht"
TOPIC_RELAY = "greenhouse/relay"
TOPIC_BUTTON = "greenhouse/button"

class GreenhouseGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # MQTT client setup
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Greenhouse_GUI")
        self.client.on_message = self.on_message
        self.client.connect(BROKER, PORT, 60)
        self.client.subscribe(TOPIC_DHT)
        self.client.subscribe(TOPIC_RELAY)
        self.client.loop_start()

    def initUI(self):
        self.setWindowTitle("Smart Greenhouse Monitor")

        # Labels for temperature, humidity, and irrigation system status
        self.temperature_label = QLabel("Temperature: -- C", self)
        self.humidity_label = QLabel("Humidity: -- %", self)
        self.relay_status_label = QLabel("Irrigation System: OFF", self)

        # Manual control buttons for irrigation system
        self.btn_irrigation_on = QPushButton('Turn Irrigation ON', self)
        self.btn_irrigation_on.clicked.connect(self.turn_irrigation_on)

        self.btn_irrigation_off = QPushButton('Turn Irrigation OFF', self)
        self.btn_irrigation_off.clicked.connect(self.turn_irrigation_off)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.relay_status_label)
        layout.addWidget(self.btn_irrigation_on)  # Add ON button to the layout
        layout.addWidget(self.btn_irrigation_off)  # Add OFF button to the layout

        self.setLayout(layout)
        self.resize(300, 200)

    # Handle incoming MQTT messages
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        
        if topic == TOPIC_DHT:
            temp_hum = payload.split(", ")
            self.temperature_label.setText(temp_hum[0])
            self.humidity_label.setText(temp_hum[1])
        elif topic == TOPIC_RELAY:
            self.relay_status_label.setText(f"Irrigation System: {payload}")

    # Function to manually turn irrigation ON
    def turn_irrigation_on(self):
        self.client.publish(TOPIC_BUTTON, "ON")  # Publish ON state to the button topic
        print("Manual button: Irrigation turned ON")

    # Function to manually turn irrigation OFF
    def turn_irrigation_off(self):
        self.client.publish(TOPIC_BUTTON, "OFF")  # Publish OFF state to the button topic
        print("Manual button: Irrigation turned OFF")

def main():
    app = QApplication(sys.argv)
    ex = GreenhouseGUI()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
