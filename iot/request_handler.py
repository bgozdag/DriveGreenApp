import requests
from enum import Enum


class ServerError(Exception):
    pass


class RequestResult(Enum):
    SUCCESS = "Success"
    SERVER_ERROR = "ServerError"
    HTTP_ERROR = "HTTPError"
    CONNECTION_ERROR = "ConnectionError"
    TIMEOUT = "Timeout"
    REQUEST_EXCEPTION = "RequestException"
    OTHER_ERROR = "OtherError"


# decorator for request functions
def handle_request_reponse(func):
    def wrapper(self, *args, **kwargs):
        try:
            json_data = {}
            response = func(self, *args, **kwargs)
            response.raise_for_status()
            RequestHandler.handle_server_result(response.json())
            json_data = response.json()
            result = RequestResult.SUCCESS
        except ServerError as err:
            print(err)
            result = RequestResult.SERVER_ERROR
        except requests.exceptions.HTTPError as err:
            print(err)
            result = RequestResult.HTTP_ERROR
        except requests.exceptions.ConnectionError as err:
            print(err)
            result = RequestResult.CONNECTION_ERROR
        except requests.exceptions.Timeout as err:
            print(err)
            result = RequestResult.TIMEOUT
        except requests.exceptions.RequestException as err:
            print(err)
            result = RequestResult.REQUEST_EXCEPTION
        except Exception as err:
            print(err)
            result = RequestResult.OTHER_ERROR
        finally:
            print("{}: {}".format(func.__name__, result))
            return(result, json_data)
    return wrapper


class RequestHandler:
    def __init__(self, base_url, headers={'Content-Type': 'application/json; charset=utf-8'}, timeout=30) -> None:
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    @staticmethod
    def handle_server_result(json_message):
        if json_message["message"] != "success":
            raise(ServerError(json_message["message"]))

    @handle_request_reponse
    def astros(self, data=None):
        path = "/astros.json"
        return requests.get(self.base_url + path, timeout=self.timeout, headers=self.headers)

    @handle_request_reponse
    def astro(self, data=None):
        path = "/astro.json"
        return requests.get(self.base_url + path, timeout=self.timeout, headers=self.headers)
