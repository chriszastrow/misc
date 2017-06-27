'''This is my MQTT Paho client used for basic interaction with a Mosquitto broker server.'''
from __future__ import print_function #fix for 2/3 print
import sys
import time
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    # Set connection status flag:
    if rc == 0:
        client_instance.connection_good = True
        print("alert: Connection success. Code: ", rc)
    else:
        client_instance.connection_bad = True #Detect authentication error.
        print("alert: Connection failure. Code: ", rc)


def on_log(client, userdata, level, buf):
    print("log: ", buf)


def on_disconnect(client, userdata,flags, rc=0):
    print("alert: Client disconnected. Code: ", rc)


def on_message(client, userdata, msg):
    # Callback when client receives PUBLISH from broker:
    subscription_payload.append(msg.payload) # Store payload in array
    print("alert: ", client_instance._client_id, "received: ", msg.topic, " ", msg.payload)


def do_publish(counter):
    # Send a PUBLISH message to the broker:
    if not publish_target and not 0:
        print("alert: ", client_instance._client_id, "publish target is empty. Publish attempt cancelled.")
    else:
        client_instance.publish(publish_target, publish_payload)
        print("alert: ", client_instance._client_id, "published: ",  publish_payload, " Counter: ", counter)


def do_subscribe(subscribe_target):
    # Send topic subscription request to the broker, wildcards # or + :
    client_instance.subscribe(subscribe_target)
    print("alert: ", client_instance._client_id, "is subscribing to: ",  subscribe_target[0][0])


def on_subscribe(client, userdata, mid, granted_qos):
    #TODO: increment target & qos when multiple subscribe targets:
    print("alert: Subscribed to ", subscribe_target[0][0], " with  QOS ", granted_qos[0])


def connect():
    #Detect network connection error:
    try:
        client_instance.connect(connection_target, 1883, 60)
    except:
        print("alert: Network connection failed.")
        sys.exit(1)


def connect_confirm():
    #Loop to check flags for errors:
    while not client_instance.connection_good:
        print("alert: Waiting for connection confirmation.")
        time.sleep(0.2)
        if client_instance.connection_bad:
            client_instance.loop_stop()
            sys.exit(1)
    print("alert: ", client_instance._client_id, " is confirmed as connected to the broker at ", connection_target)


def main_loop():
    # Set publish conditions here:
    counter = 0
    while counter < 1:
        do_publish(counter)
        counter += 1
        time.sleep(5)


def init(): 
    #Initialize flags:
    mqtt.Client.connection_good = False
    mqtt.Client.connection_bad = False
    #Connect callbacks:
    client_instance.on_log = on_log
    client_instance.on_connect = on_connect
    client_instance.on_message = on_message
    client_instance.on_subscribe = on_subscribe
    client_instance.on_disconnect = on_disconnect


#Init global variables:
connection_target = "test.mosquitto.org" #"iot.eclipse.org"
client_instance = mqtt.Client("MyClient", clean_session=True, userdata=None, \
    protocol=mqtt.MQTTv311, transport="tcp") #clean_session clears subscriptions on disconnect.
subscription_payload = [] #Subscription records collected in list.
subscribe_target = [("broker/test", 1)] #Supports multiple subscription targets as list of tuples with QOS value.
publish_target = "broker/test" #TODO add multiple publish target support (with QOS etc) via dict.
publish_payload = "This is a test of the MQTT publishing system."

init()
connect()
client_instance.loop_start() #The "loop" activates processing of callbacks, which will not be caught otherwise.
connect_confirm()
do_subscribe(subscribe_target) #TODO: Consider if subscription confirmation is required before proceeding.
main_loop() #Do any publishing in here.

client_instance.disconnect()
client_instance.loop_stop()
#client_instance.loop_forever()
