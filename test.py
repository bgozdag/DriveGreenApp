from iot.request_handler import RequestResult
from iot.server_handler import ServerHandler
import unittest


class Test(unittest.TestCase):
    def test_astros(self):
        server_handler = ServerHandler('http://api.open-notify.org')
        self.assertEqual(server_handler.test_procedure(),
                         RequestResult.HTTP_ERROR)
        self.assertNotEqual(server_handler.test_procedure(),
                            RequestResult.SUCCESS)


if __name__ == "__main__":
    unittest.main()