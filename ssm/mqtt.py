# import paho.mqtt.client as mqtt
# from . import settings

# def on_connect(mqtt_client, userdata, rc, properties=None):
#     res = rc['session present']
#     if res == 0:
#        print('Connected successfully')
#     else:
#         print('Bad connection. Code:', rc)

#     mqtt_client.subscribe('django/mqtt')


# def on_message(mqtt_client, userdata, msg):
#     print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
# client.connect(
#     host=settings.MQTT_SERVER,
#     port=settings.MQTT_PORT,
#     keepalive=settings.MQTT_KEEPALIVE
# )
# # client.connect("iot.eclipse.org", 1883, 60)
