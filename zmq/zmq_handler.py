from typing import Callable
import zmq
from threading import Thread
import time
from queue import Queue

class ZmqHandler(Thread):
    def __init__(self, on_message_received: Callable, ip="127.0.0.1", port="5565") -> None:
        super().__init__()
        context = zmq.Context()
        self.on_message_received = on_message_received
        self.socket = context.socket(zmq.DEALER)
        self.socket.setsockopt_string(zmq.IDENTITY, "DriveGreenApp")
        self.socket.connect("tcp://{0}:{1}".format(self.ip, self.port))
        self.dealer_queue = Queue()

    def send(self, msg):
        self.dealer_queue.put(msg)

    def run(self):
        while True:
            if self.socket.poll(10) == zmq.POLLIN:
                try:
                    msg = self.socket.recv_string()
                    self.on_message_received(msg)
                except:
                    time.sleep(0.05)
                    continue

            if not self.dealer_queue.empty():
                msg = self.dealer_queue.get()
                self.socket.send_string(msg)

