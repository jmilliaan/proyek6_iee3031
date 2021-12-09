import paho.mqtt.client as mqtt
import roboconvcv_constants as constants


class MQTT:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(constants.mqtt_username, constants.mqtt_password)
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        try:
            print(f"Connected {str(rc)}")
            self.client.subscribe(constants.mqtt_topic)
            self.connected = True
        except:
            self.connected = False
            pass

    @staticmethod
    def on_message(client, userdata, msg):
        incoming = msg.payload.decode("utf-8")
        data_list = incoming.split()
        return data_list

    def begin_mqtt(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(constants.mqtt_ip, 1883)
        self.client.loop()
        self.client.disconnect()
