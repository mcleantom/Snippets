import zmq

# Prepare our context and sockets
context = zmq.Context()
frontend = context.socket(zmq.ROUTER)
backend = context.socket(zmq.DEALER)
frontend.bind("tcp://*:5560")
backend.bind("tcp://*:5561")

# Initialize poll set
poller = zmq.Poller()
poller.register(frontend, zmq.POLLIN)
poller.register(backend, zmq.POLLIN)

# Switch messages between sockets
while True:
    socks = dict(poller.poll())
    
    if socks.get(frontend) == zmq.POLLIN:
        message = frontend.recv_multipart()
        print(f"sending {message} to backend")
        backend.send_multipart(message)
    
    if socks.get(backend) == zmq.POLLIN:
        message = backend.recv_multipart()
        print(f"sending {message} to frontend")
        frontend.send_multipart(message)
