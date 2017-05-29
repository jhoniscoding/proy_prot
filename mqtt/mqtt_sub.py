import paho.mqtt.client as mqtt
import monotonic

topic = "testing"
#hostname = "localhost"
#hostname = "192.168.0.16"
hostname = "104.154.178.21"

def on_connect(client, userdata, flags, rc):
    print("waiting for messages...")

def on_message(client, userdata, message):
    global iter
    msg_data = message.payload.decode('ascii').split()
    id = int(msg_data[0])
    latency = (monotonic.monotonic() - float(msg_data[1])) * 1000
    payload_len = len(message.payload)
    write("%d %s" %(payload_len, latency))
    print('%d: (%d bytes) received in %f ms' %(id, payload_len, latency))
    if id == n:
        iter += 1
    if(iter == m):
        client.disconnect()

def write(line):
    with open("latencies.txt", 'a') as input:
        input.write("%s\n" %line)

with open("../config", 'r') as conf:
    m, n = [int(i) for i in conf.readline().split()[:2]]
    iter = 0

client = mqtt.Client(client_id="subscriber")
client.on_message = on_message
client.on_connect = on_connect
client.connect(hostname)
client.subscribe(topic, 0)
client.loop_forever()
