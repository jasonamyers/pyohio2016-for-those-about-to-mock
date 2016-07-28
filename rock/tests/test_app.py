import unittest

from rock.app import hello_world


class TestFlaskApp(unittest.TestCase):

    def test_hello_world(self):
        result = hello_world()
        self.assertDictEqual({'message': 'Hello World'}, result)
