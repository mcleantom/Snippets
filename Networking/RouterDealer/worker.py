import zmq
import time
from uuid import uuid4

context = zmq.Context()
client = context.socket(zmq.DEALER)
identity = str(uuid4())
client.identity = identity.encode("ascii")
client.connect("tcp://localhost:5560")

poller = zmq.Poller()
poller.register(client, zmq.POLLIN)

for request_num in range(10):
    print("Sending request %s to broker" % request_num)
    client.send_multipart([b'Hello', b'World'])

    socks = dict(poller.poll(5000))  # Timeout set to 5000 milliseconds (5 seconds)

    if client in socks:
        message = client.recv()
        print("Received reply %s [ %s ]" % (request_num, message))
    else:
        print("No response from broker for request %s" % request_num)

    time.sleep(1)

poller.unregister(client)
client.close()
context.term()
