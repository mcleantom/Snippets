import time
import uuid
from concurrent.futures import ProcessPoolExecutor

import zmq
from loguru import logger

from FlowField.zmq.job import Job

WORKER_HOST = "127.0.0.1"
WORKER_PORT = 5755


class Worker:
    def __init__(self, host: str = WORKER_HOST, port: int = WORKER_PORT):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.host = host
        self.port = port
        self.socket_id = str(uuid.uuid4())
        self.socket.setsockopt_string(zmq.IDENTITY, self.socket_id)
        self.socket.connect(f"tcp://{self.host}:{self.port}")
        logger.info("Worker connected")

        self.run()

    @staticmethod
    def do_work(work):
        result = work["number1"] ** 2 + work["number2"]
        time.sleep(work["number1"])
        return result

    def disconnect(self):
        self.socket.send_json({"worker_id": self.socket_id, "message": "disconnect"})
        self.socket.close()
        self.context.term()

    def run(self):
        self.socket.send_json({"worker_id": self.socket_id, "message": "connect"})
        while True:
            job = self.socket.recv_json()
            logger.debug(f"{self.socket_id} received task")
            value = self.do_work(job)
            self.socket.send_json(
                {"worker_id": self.socket_id, "message": "job_done", "job": Job.get_result(job, value)}
            )


def work():
    Worker()


if __name__ == "__main__":
    futures = []
    with ProcessPoolExecutor() as f:
        for _ in range(5):
            future = f.submit(work)
            futures.append(future)
