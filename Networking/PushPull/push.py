import json
import uuid
from typing import Dict

import zmq

__all__ = ["Push"]


class Push:
    def __init__(self, uid: uuid.UUID, server_address: str):
        """
        A blocking client to push data to one server.

        :param uid: Uniquely identifies where the data is coming from
        :param server_address: The address of the server to send data to
        """
        self.uid = uid
        self.server_address = server_address

        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUSH)
        self._socket.connect(self.server_address)

    def send_dict(self, d: Dict) -> None:
        """
        Sends a dictionary as a JSON message

        :param d: Dictionary to send
        :return:
        """
        d_as_bytes = json.dumps(d, indent=2).encode("utf-8")
        self._send(d_as_bytes)

    def send_string(self, s: str) -> None:
        """
        Sends a string as a JSON message in the format {"message": s}

        :param s: String to send
        """
        d = {"message": s}
        d_as_bytes = json.dumps(d, indent=2).encode("utf-8")
        self._send(d_as_bytes)

    def _send(self, data) -> None:
        self._socket.send_multipart([self.uid.bytes, data])
