import sys

def mean(array):
    return sum(array) / len(array)

with open("config", 'r') as conf, open(sys.argv[1], 'r') as lat, open(sys.argv[2], 'r') as sm, open(sys.argv[3], 'w') as met:
    n, s = [int(i) for i in conf.readlines()[0].split()[:-1]]

    for i in range(n):
        pay_len = 0
        lats = []
        sms = {
            "send":[],
            "cpu_time":[],
            "cpu_usg":[]
        }
        for j in range(s):
            lat_data = lat.readline().split()
            pay_len = lat_data[0]
            lats.append(float(lat_data[1]))
            sm_data = [float(i) for i in sm.readline().split()]
            sms['send'].append(sm_data[0])
            sms['cpu_time'].append(sm_data[1])
            sms['cpu_usg'].append(sm_data[2])
        line = "%s %s %s %s %s\n" %(pay_len, mean(lats), mean(sms['send']), mean(sms['cpu_time']), mean(sms['cpu_usg']))
        met.write(line)
