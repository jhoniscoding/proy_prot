import sys
import matplotlib.pyplot as plt
import numpy as np

MB = 1048576

data = {
    "lens": [],
    "cpu_times": [],
    "sending_times": [],
    "cpu_usages": [],
    "lats": []
}
data_packets = {
    "lens": [],
    "bytes_trans": [],
    "packets": [],
    "avg_packet_size": []
}
oper_costs = {
    "movistar": 63/MB,
    "tigo": 153/MB,
    "virgin": 160/MB,
    "claro": 399/MB
}
data_oper = {
    "movistar": [],
    "tigo": [],
    "virgin": [],
    "claro": []
}

with open("files",'r') as files:
    fs = [f.rstrip() for f in files.readlines()]
    file_times = []
    file_lens = []
    for i in range(len(fs)):
        if fs[i]=="":
            break
    file_times = fs[:i]
    file_lens = fs[(i+1):]

legends = [f.split('_')[0].upper() for f in file_times]

def build_times_data():
    for file in file_times:
        with open(file, 'r') as met:
            lines = met.readlines()
            lens = []
            cpu_times = []
            sending_times = []
            cpu_usages = []
            lats = []
            for line in lines:
                met_data = line.split()
                lens.append(met_data[0])
                lats.append(met_data[1])
                sending_times.append(met_data[2])
                cpu_times.append(met_data[3])
                cpu_usages.append(met_data[4])
            data['lens'].append(lens)
            data['lats'].append(lats)
            data['sending_times'].append(sending_times)
            data['cpu_times'].append(cpu_times)
            data['cpu_usages'].append(cpu_usages)

def build_packets_data():
    for file in file_lens:
        with open(file, 'r') as met:
            lines = met.readlines()
            lens = []
            bytes_trans = []
            packets = []
            avg_packet_size = []
            movistar = []
            tigo = []
            virgin = []
            claro = []
            for line in lines:
                met_data = line.split()
                bt = int(met_data[1])
                lens.append(int(met_data[0]))
                bytes_trans.append(bt)
                packets.append(int(met_data[2]))
                avg_packet_size.append(int(met_data[3]))
                movistar.append(oper_costs["movistar"]*bt)
                tigo.append(oper_costs["tigo"]*bt)
                virgin.append(oper_costs["virgin"]*bt)
                claro.append(oper_costs["claro"]*bt)
            data_packets['lens'].append(lens)
            data_packets['packets'].append(packets)
            data_packets['bytes_trans'].append(bytes_trans)
            data_packets['avg_packet_size'].append(avg_packet_size)
            data_oper["movistar"].append(movistar)
            data_oper["tigo"].append(tigo)
            data_oper["virgin"].append(virgin)
            data_oper["claro"].append(claro)

def draw_times_plot():
    plt.figure(1)

    plt.subplot(221)
    plt.grid()
    plt.title("CPU Average Times")
    plt.xlabel("Payload (bytes)")
    plt.ylabel("Time (ms)")
    for i in range(len(data['lens'])):
        plt.plot(data["lens"][i], data["cpu_times"][i], label=legends[i])
    plt.legend(loc="upper left")

    plt.subplot(222)
    plt.grid()
    plt.title("Sending Average Times")
    plt.xlabel("Payload (bytes)")
    plt.ylabel("Time (ms)")
    for i in range(len(data['lens'])):
        plt.plot(data["lens"][i], data["sending_times"][i], label=legends[i])
    plt.legend(loc="upper left")

    plt.subplot(223)
    plt.grid()
    plt.title("CPU Usage Average Times")
    plt.xlabel("Payload (bytes)")
    plt.ylabel("Usage (%)")
    for i in range(len(data['lens'])):
        plt.plot(data["lens"][i], data["cpu_usages"][i], label=legends[i])
    plt.legend(loc="upper left")

    plt.subplot(224)
    plt.grid()
    plt.title("Latency Average Times")
    plt.xlabel("Payload (bytes)")
    plt.ylabel("Time (ms)")
    for i in range(len(data['lens'])):
        plt.plot(data["lens"][i], data["lats"][i], label=legends[i])
    plt.legend(loc="upper left")

def draw_packets_plot():

    plt.figure(2)

    plt.subplot(221)
    plt.grid()
    plt.xlabel("Payload (bytes)")
    plt.ylabel("Bytes Transferred")
    for i in range(len(data_packets['lens'])):
        plt.plot(data_packets["lens"][i], data_packets["bytes_trans"][i], label=legends[i])
    plt.legend(loc="upper left")

    plt.subplot(222)
    plt.grid()
    plt.xlabel("Payload (bytes)")
    plt.ylabel("Packets Sent")
    for i in range(len(data_packets['lens'])):
        plt.plot(data_packets["lens"][i], data_packets["packets"][i], label=legends[i])
    plt.legend(loc="upper left")

    plt.subplot(223)
    plt.grid()
    plt.xlabel("Payload (bytes)")
    plt.ylabel("Average Packet Size (bytes)")
    for i in range(len(data_packets['lens'])):
        plt.plot(data_packets["lens"][i], data_packets["avg_packet_size"][i], label=legends[i])
    plt.legend(loc="upper left")

    plt.subplot(224)
    plt.grid()
    plt.xlabel("Average Bytes Transferred")
    plt.ylabel("Money (COP)")
    plt.plot(data_packets["lens"][1], data_oper["tigo"][1], label="Tigo")
    line = plt.plot(data_packets["lens"][1], data_oper["virgin"][1], label="Virgin")
    plt.setp(line, color='m')
    plt.plot(data_packets["lens"][1], data_oper["movistar"][1], label="Movistar")
    plt.plot(data_packets["lens"][1], data_oper["claro"][1], label="Claro")
    plt.legend(loc="upper left")

build_times_data()
build_packets_data()
draw_times_plot()
draw_packets_plot()
plt.show()
