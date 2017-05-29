from coapthon.client.helperclient import HelperClient
from time import sleep
from os import getpid, sysconf_names, sysconf

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
    time_elapsed = (get_uptime() - (start_time / hertz)) * 1000
    cpu_usage = 100 * (cpu_time / time_elapsed)
    return time_elapsed, cpu_time, cpu_usage

def get_uptime():
    with open("/proc/uptime", 'r') as up:
        return float(up.readline().split()[0])

def write(filename, line):
    with open(filename, 'a') as input:
        input.write("%s\n" %line)

hostname = "127.0.0.1"
port = 5683
resource = "testing"

client = HelperClient(server=(hostname, port))

with open("config", 'r') as conf:
    m, n, delay = [int(i) for i in conf.readline().split()]

for i in range(m):
    msg = 'a'*(2**i)
    for j in range(n):
        id = j + 1
        payload = "%s" %msg
        payload_len = len(payload)
        initial_metrics = get_metrics()
        client.put(resource, payload)
        metrics = get_metrics()
        times = [metrics[i] - initial_metrics[i] for i in range(len(metrics))]
        write("some_metrics.txt", "%s" %' '.join([str(i) for i in times]))
        print("%d: (%d bytes) sent in %f ms!" %(id, payload_len, times[0]))

        sleep(delay)

        uptime = get_uptime()
        client.get(resource)
        latency = ((get_uptime() - uptime) * 1000) + times[0]
        write("latencies.txt", "%s %s" %(payload_len, latency))
        print("%d: (%d bytes) received in %f ms!\n" %(id, payload_len, latency))

client.stop()
