from paho.mqtt import publish
from .settings import MQTT_AUTH


def send_command_to_device(topic, messasge):
    publish.single(topic=topic, payload=messasge, auth=MQTT_AUTH)