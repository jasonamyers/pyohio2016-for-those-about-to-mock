import unittest
from collections import namedtuple
from io import BytesIO

from mock import MagicMock, call, patch

from app import hello_world
from dal import process_results, process_file


class TestApp(unittest.TestCase):

    def test_hello_world(self):
        result = hello_world()
        self.assertDictEqual({'message': 'Hello World'}, result)


class TestDal(unittest.TestCase):

    def test_process_results_not_found(self):
        Faker = namedtuple("Faker", ['status_code', ])
        test_object = Faker(status_code=404)
        result = process_results(test_object)
        self.assertDictEqual({'message': 'Rock Not found!'}, result)

    def test_process_results_success(self):
        test_object = MagicMock()
        test_object.status_code = 200
        test_object.json.return_value = {'message': 'This is just a tribute!'}
        result = process_results(test_object)
        self.assertDictEqual({'message': 'This is just a tribute!'}, result)
        expected_calls = [call.json()]
        self.assertListEqual(expected_calls, test_object.mock_calls)

    def test_process_results_bad_status(self):
        test_object = MagicMock()
        test_object.status_code = 'cookies'
        self.assertRaises(ValueError, process_results, test_object)

        expected_calls = []
        self.assertListEqual(expected_calls, test_object.mock_calls)

    def test_process_results_bad_status_message(self):
        test_object = MagicMock()
        test_object.status_code = 'cake'
        with self.assertRaises(ValueError) as exc_info:
            process_results(test_object)

            self.assertTrue('SHARON!' in exc_info.exception)

        expected_calls = []
        self.assertListEqual(expected_calls, test_object.mock_calls)

    def test_process_results_bad_json_call(self):
        test_object = MagicMock()
        test_object.status_code = 200
        test_object.json.side_effect = ValueError('Nickleback')
        with self.assertRaises(ValueError) as exc_info:
            process_results(test_object)

            self.assertTrue('Nickleback' in exc_info.exception)

        expected_calls = [call.json()]
        self.assertListEqual(expected_calls, test_object.mock_calls)

    @patch('__builtin__.open')
    def test_process_file(self, open_mock):
        fake_file = BytesIO(b'Joan Jett\nJanis Joplin\nAlanis Morissette')
        expected_results = ['Joan Jett', 'Janis Joplin', 'Alanis Morissette']
        open_mock.return_value = fake_file
        results = process_file('cookies.csv')

        self.assertListEqual(expected_results, results)
