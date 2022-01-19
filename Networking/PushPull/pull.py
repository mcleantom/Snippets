import asyncio
import json
import traceback
import uuid
from typing import Callable, Dict, Union

import zmq
import zmq.asyncio
from BATDataModels.Mongo.routing_server import ClientInfo

__all__ = ["Pull"]


class Pull:
    def __init__(self, *, protocol: str, interface: str, port: Union[str, int]):
        """
        An asynchronous server to receive messages from many clients

        :param protocol: The protocol of the server
        :param interface: The interface of the server
        :param port: The port of the server
        """
        self.protocol = protocol
        self.interface = interface
        self.port = port

        self._context = zmq.asyncio.Context()
        self._socket = self._context.socket(zmq.PULL)
        self._socket.bind(self.address)

        self._running = False

        self._received_messages: Dict[uuid.UUID, Dict] = {}
        self._callbacks: Dict[uuid.UUID, Callable] = {}

    @classmethod
    def from_config(cls, config: ClientInfo):
        return cls(**config.dict())

    @property
    def address(self):
        return f"{self.protocol}://{self.interface}:{self.port}"

    def run(self) -> None:
        asyncio.create_task(self.message_loop(), name="Message loop")

    def shutdown(self) -> None:
        self._running = False
        self._socket.close()
        self._context.term()

    def add_callback(self, uid: uuid.UUID, fn: Callable) -> None:
        """
        Add a callback after receiving a message from a particular client

        :param uid: The unique identifier of the client
        :param fn: The function to run after receiving the message. The function will receive the uid and the JSON data.
        """
        self._callbacks[uid] = fn

    def delete_callback(self, uid: uuid.UUID):
        """
        Delete a callback after receiving a message from a particular client

        :param uid: The unique identifier of the client
        """
        del self._callbacks[uid]

    async def message_loop(self):
        if self._running:
            print("Already running...")
            raise RuntimeError("We are already running")

        try:
            self._running = True

            while self._running:
                try:
                    topic, msg = await self._socket.recv_multipart()
                except zmq.ZMQError:
                    traceback.print_exc()
                else:
                    uid = uuid.UUID(bytes=topic)
                    data = json.loads(msg.decode("utf-8"))
                    self._received_messages[uid] = data

                    if uid in self._callbacks:
                        await self._callbacks[uid](uid, data)

        except Exception:
            traceback.print_exc()
        finally:
            self._running = False
