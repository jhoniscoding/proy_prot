import pika
import monotonic

def on_message(ch, method, properties, body):
    global iter
    msg_data = body.decode('ascii').split()
    id = int(msg_data[0])
    latency = (monotonic.monotonic() - float(msg_data[1])) * 1000
    payload_len = len(body)
    write("%d %s" %(payload_len, latency))
    print('%d: (%d bytes) received in %f ms!' %(id, payload_len, latency))
    if id == n:
        iter += 1
    if iter == m:
        ch.stop_consuming()
        connection.close()

def write(line):
    with open("latencies.txt", 'a') as input:
        input.write("%s\n" %line)

with open("../config", 'r') as conf:
    m, n, delay = [int(i) for i in conf.readline().split()]
    iter = 0

#hostname = "localhost"
hostname = "104.154.178.21"
credentials = pika.PlainCredentials('admin', 'LaraCroft')
connection = pika.BlockingConnection(pika.ConnectionParameters(hostname, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue="testing")
channel.basic_consume(on_message, queue="testing", no_ack=True)
print("waiting for messages...")
channel.start_consuming()
