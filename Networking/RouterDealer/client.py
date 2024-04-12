import random
import uuid

import zmq
from loguru import logger

from FlowField.zmq.job import Job

NUMBER_OF_MESSAGES_SENT = 4
WAIT_TIME = 0
CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = 5754


class Client:
    def __init__(self, host: str = CLIENT_HOST, port: int = CLIENT_PORT):
        self.context = zmq.Context()
        self.host = host
        self.port = port
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.bind("tcp://%s:%d" % (self.host, self.port))
        self.identity = str(uuid.uuid4())
        self.socket.setsockopt_string(zmq.IDENTITY, self.identity)
        self.run()

    def run(self):
        poll = zmq.Poller()
        poll.register(self.socket, zmq.POLLIN)

        numbers = [0.1, 2]

        jobs = {}

        for number in numbers:
            job_id = str(number)
            job = Job({"number1": number, "number2": random.randint(0, 100)}, job_id)
            self.socket.send_json({"client_id": self.identity, "message": "connect", "job": job.get_job()})
            jobs[job_id] = job

        while True:
            sockets = dict(poll.poll())
            if self.socket in sockets:
                response = self.socket.recv_multipart()
                job = jobs[response[0].decode()]
                number1 = job.payload["number1"]
                logger.debug(f"received {response}, {number1=}")
                self.socket.send_json({"client_id": self.identity, "message": "connect", "job": job.get_job()})


if __name__ == "__main__":
    Client()
