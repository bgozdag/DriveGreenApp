from email.mime import base
from unittest import result
from .request_handler import RequestResult, RequestHandler

class ServerHandler:
    def __init__(self, base_url) -> None:
        self.base_url = base_url

    def test_procedure(self):
        result, data = RequestHandler(self.base_url).astros()
        if result != RequestResult.SUCCESS:
            return result
        result, data = RequestHandler(self.base_url).astro()
        return result