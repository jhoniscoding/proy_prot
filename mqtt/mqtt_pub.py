import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from os import getpid, sysconf_names, sysconf
from time import sleep

topic = "testing"
#hostname = "localhost"
#hostname = "192.168.0.16"
hostname = "104.154.178.21"
payload = ""

def on_connect(client, userdata, flags, rc):
    print("Connected to: %s/%s\n" %(hostname, topic))

def on_publish(client, userdata, mid):
    metrics = get_metrics()
    times = [metrics[i] - initial_metrics[i] for i in range(len(metrics))]
    write("%s" %' '.join([str(i) for i in times]))
    print("%s sent in %f ms" %(mid, times[0]))

def get_metrics():
    with open("/proc/%s/stat"%getpid(), 'r') as times:
        times_data = times.readline().split()
        utime = int(times_data[13])
        stime = int(times_data[14])
        cutime = int(times_data[15])
        cstime = int(times_data[16])
        start_time = int(times_data[21])
        hertz = sysconf(sysconf_names['SC_CLK_TCK'])
    cpu_time = (float(utime + stime + cutime + cstime) / hertz) * 1000
    time_elapsed = (float(get_uptime()) - (start_time / hertz)) * 1000
    cpu_usage = 100 * (cpu_time / time_elapsed)
    return time_elapsed, cpu_time, cpu_usage

def get_uptime():
    with open("/proc/uptime", 'r') as up:
        return up.readline().split()[0]

def write(line):
    with open("some_metrics.txt", 'a') as input:
        input.write("%s\n" %line)

client = mqtt.Client(client_id="publisher")
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(hostname)
client.loop_start()

with open("../config", 'r') as conf:
    m, n, delay = [int(i) for i in conf.readline().split()]

for i in range(m):
    msg = 'a'*(2**i)
    for j in range(n):
        initial_metrics = get_metrics()
        id = j + 1
        uptime = get_uptime()
        uptime = uptime + '0' if len(uptime.split('.')[1]) == 1 else uptime
        payload = "%s %s %s"%(str(id).zfill(len(str(n))), uptime, msg)
        client.publish(topic, payload)
        sleep(delay)

client.loop_stop()
client.disconnect()
