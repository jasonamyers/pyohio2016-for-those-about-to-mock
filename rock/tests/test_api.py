from flask_testing import LiveServerTestCase
import requests

from rock.app import app

class ApiTest(LiveServerTestCase):

    def create_app(self):
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def test_hello_endpoint(self):
        response = requests.get(self.get_server_url() + '/hello/')
        self.assertEqual(response.status_code, 200)

    def test_rock_endpoint(self):
        response = requests.get(self.get_server_url() + '/rock/')
        self.assertEqual(response.status_code, 200)
        assert 1 == response.json()[0]['userId']
