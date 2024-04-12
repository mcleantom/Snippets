import zmq

context = zmq.Context()
worker = context.socket(zmq.DEALER)
worker.connect("tcp://localhost:5561")

while True:
    message = worker.recv_multipart()
    print("Received message from broker:", message)
    # Process the message here
    # ...
    # Respond back to the broker
    response = b"Processed: " + message[1]
    worker.send_multipart([message[0], response])
