import json
from collections import deque

import zmq
from loguru import logger

MAX_JOBS_PER_WORKER = 1
FRONTEND_HOST = "127.0.0.1"
FRONTEND_PORT = 5754
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 5755
SINK_HOST = "127.0.0.1"
SINK_PORT = 5758


class Broker:
    def __init__(
        self,
        backend_host: str = BACKEND_HOST,
        backend_port: int = BACKEND_PORT,
        frontend_host: str = FRONTEND_HOST,
        frontend_port: int = FRONTEND_PORT,
    ):
        logger.info("Starting broker")
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.frontend_host = frontend_host
        self.frontend_port = frontend_port
        self.context = zmq.Context()
        self.backend = self.context.socket(zmq.ROUTER)
        self.backend.bind("tcp://%s:%d" % (self.backend_host, self.backend_port))

        self.frontend = self.context.socket(zmq.ROUTER)
        self.frontend.connect("tcp://%s:%d" % (self.frontend_host, self.frontend_port))

        self.ready_workers = deque()
        self.work_queue = deque()

        self.worker_id_to_client_id = {}

        self.max_jobs_per_worker = MAX_JOBS_PER_WORKER
        self.work_to_requeue = deque()
        self.backend_result = self.backend

        self.poller = zmq.Poller()
        self.poller.register(self.backend, zmq.POLLIN)
        self.poller.register(self.frontend, zmq.POLLIN)

        self.run()

    def get_next_worker_id(self):
        if len(self.ready_workers) == 0:
            return None
        return self.ready_workers.popleft()

    def process_results(self, worker_id: str, job: dict) -> None:
        job_id = job["id"]
        result = job["result"]
        logger.info(f"Worker {worker_id} finished job {job_id} with result {result}")
        self.frontend.send_multipart([self.worker_id_to_client_id[worker_id], job["name"].encode()])
        self.ready_workers.append(worker_id)

    def handle_worker_message(self, worker_id: str, message: dict) -> None:
        if message["message"] == "connect":
            self.ready_workers.append(worker_id)
        elif message["message"] == "disconnect":
            pass
        elif message["message"] in ["job_done", "job_failed"]:
            job = message["job"]
            self.process_results(worker_id, job)

    def handle_client_message(self, client_id, request: dict) -> None:
        if request["message"] == "connect":
            self.work_to_requeue.append((client_id, request["job"]))
        else:
            logger.warning(f"Unhandled client request {request}")

    def run(self):
        while True:
            logger.debug("Checking for messages")
            sockets = dict(self.poller.poll())

            if self.backend in sockets:
                worker_id, *message = self.backend.recv_multipart()
                logger.debug(f"{worker_id} {message}")
                message = json.loads(message[0].decode())
                logger.debug(f"Received message from worker {worker_id}")
                self.handle_worker_message(worker_id, message)

            if self.frontend in sockets:
                client_id, *message = self.frontend.recv_multipart()
                request = json.loads(message[0].decode("utf-8"))
                logger.debug(f"Received message from frontend {client_id}")
                self.handle_client_message(client_id, request)

            if len(self.ready_workers) and self.work_to_requeue:
                next_worker_id = self.ready_workers.popleft()
                client_id, job = self.work_to_requeue.popleft()
                logger.debug(f"Sending job {job} to worker {next_worker_id}")
                self.backend.send_multipart([next_worker_id, json.dumps(job).encode("utf-8")])
                self.worker_id_to_client_id[next_worker_id] = client_id


if __name__ == "__main__":
    Broker()
