import pika
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
    time_elapsed = (float(get_uptime()) - (start_time / hertz)) * 1000
    cpu_usage = 100 * (cpu_time / time_elapsed)
    return time_elapsed, cpu_time, cpu_usage

def get_uptime():
    with open("/proc/uptime", 'r') as up:
        return up.readline().split()[0]

def write(line):
    with open("some_metrics.txt", 'a') as input:
        input.write("%s\n" %line)

#hostname = "localhost"
hostname = "104.154.178.21"
credentials = pika.PlainCredentials('admin', 'LaraCroft')
connection = pika.BlockingConnection(pika.ConnectionParameters(hostname, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue="testing")

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
        channel.basic_publish(exchange='', routing_key="testing", body=payload)
        metrics = get_metrics()
        times = [metrics[i] - initial_metrics[i] for i in range(len(metrics))]
        write("%s" %' '.join([str(i) for i in times]))
        print("%d: (%d bytes) sent in %f ms!" %(id, len(payload), times[0]))
        sleep(delay)

connection.close()
