# (c) Simen Sommerfeldt, @sisomm, simen.sommerfeldt@gmail.com Licensed as CC-BY-SA 
import time
import os
import argparse
import json
import paho.mqtt.client as paho
import microbit	

parser = argparse.ArgumentParser()
parser.add_argument("-t","--topic", default="/microbit/0", help="The base MQTT topic")
parser.add_argument("-s","--server", default="127.0.0.1", help="The IP address of the MQTT server")
parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1],  default=0,
                    help="increase output verbosity")
args = parser.parse_args()

def on_message(mosq, obj, msg):
    #called when we get an MQTT message that we subscribe to
    if(args.verbosity>0):
        print("Message received on topic "+msg.topic+" with payload "+msg.payload)


print("Connecting")
mypid = os.getpid()
client = paho.Client("microbit_"+str(mypid))
client.connect(args.server)
client.on_message = on_message
client.loop_start()

try:
    while True:
	    acctopic=args.topic+"/accelerometer"
	    print(json.dumps(microbit.accelerometer.get_values()))
            client.publish(acctopic,json.dumps(microbit.accelerometer.get_values()) ,0)
	    time.sleep(0.1)

except KeyboardInterrupt:
    client.loop_stop()
