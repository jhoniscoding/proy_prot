import monotonic
from coapthon.client.helperclient import HelperClient

#hostname = "127.0.0.1"
hostname = "104.154.178.21"
port = 5683
path = "testing"

def on_message(response):
    if response.payload and len(response.payload.split()) > 2:
        global iter
        global pkg_count
        global waiting
        global lat_sum
        msg_data = response.payload.decode('ascii').split()
        id = int(msg_data[0])
        if iter > 9:
            lat_sum += (monotonic.monotonic() - float(msg_data[1])) * 1000
            pkg_count += 1
            if pkg_count < 2**(iter - 10):
                waiting = True
            else:
                waiting = False
                latency = lat_sum/pkg_count
                payload_len = 2**(iter-10) * len(response.payload)
                save(id, payload_len, latency)
                pkg_count = 0
                lat_sum = 0
        else:
            latency = (monotonic.monotonic() - float(msg_data[1])) * 1000
            save(id, len(response.payload), latency)
        if id == n and not waiting:
            iter += 1
        if iter == m:
            client.delete(path)
            client.cancel_observing(response, True)

def save(id, payload_len, latency):
    write("%d %s" %(payload_len, latency))
    print('%d: (%d bytes) received in %f ms!' %(id, payload_len, latency))

def write(line):
    with open("latencies.txt", 'a') as input:
        input.write("%s\n" %line)

with open("../config", 'r') as conf:
    m, n, delay = [int(i) for i in conf.readline().split()]
    iter = 0
    pkg_count = 0
    waiting = False
    lat_sum = 0

client = HelperClient(server=(hostname, port))
print("waiting for messages...")
client.observe(path, on_message)
