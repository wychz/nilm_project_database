import paho.mqtt.client as mqtt
import running_param as param
import os

file_path = os.path.abspath("./plot_results/single_file/")
model_path = os.path.abspath("./saved_models/concat_1min/single_file/")
payload = "model: " + model_path + ", file: " + file_path

MQTTHOST = param.mqtt_host
MQTTPORT = param.mqtt_port
MQTTTOPIC = "/exp/" + param.experiment_id
MQTTPAYLOAD = payload
mqttClient = mqtt.Client()


def on_mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()


# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)


# 消息处理函数
def on_message_come(lient, userdata, msg):

    print(msg.topic + " " + ":" + str(msg.payload))


# subscribe 消息
def on_subscribe():
    mqttClient.subscribe("/server", 1)
    mqttClient.on_message = on_message_come # 消息到来处理函数


def publish_message():
    on_mqtt_connect()
    on_publish(MQTTTOPIC, payload, 1)
    while True:
        pass