import paho.mqtt.client as mqtt

MQTTHOST = "localhost"
MQTTPORT = 1883
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
    on_publish("/test/server", "Hello Python!", 1)
    on_subscribe()
    while True:
        pass