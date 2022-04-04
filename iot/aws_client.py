import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from utils import Path


class AWSClient(AWSIoTMQTTClient):
    def __init__(self, clientID, protocolType=..., useWebsocket=False, cleanSession=True):
        super().__init__(clientID, protocolType, useWebsocket, cleanSession)
        self.configure()
        self.set_callbacks()
        self.connect()
        self.subscribe_all()

    def configure(self):
        self.configureIAMCredentials(Path.ROOT_CA, Path.CERT, Path.PRIVATE_KEY)

    def subscribe_all(self):
        pass

    def connect(self, keepAliveIntervalSecond=600):
        super().connect(keepAliveIntervalSecond)
        print("AWSClient connected")

    def disconnect(self):
        try:
            super().disconnect()
        except:
            pass
        finally:
            print("AWSClient disconnected")

    def reconnect(self):
        print("Reconnecting AWSClient...")
        self.disconnect()
        time.sleep(.5)
        self.connect()

    def on_online(self):
        print("AWSClient online")

    def on_offline(self):
        print("AWSClient offline")

    def on_message(self, message):
        print("Received: {}".format(message.payload))

    def set_callbacks(self):
        self.onOnline = self.on_online
        self.onOffline = self.on_offline
        self.onMessage = self.on_message

    def publish(self, topic, payload, QoS=1):
        self.publishAsync(topic, payload, QoS, ackCallback=self.publish_ack)

    def publish_ack(self, packet_id):
        print("Publish ACK: {}".format(packet_id))

    def subscribe_ack(self, packet_id):
        print("Subscribe ACK: {}".format(packet_id))
