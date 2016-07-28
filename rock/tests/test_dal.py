import os

import betamax
from betamax import Betamax
from mock import patch
import requests
from requests import ConnectionError

from rock.dal import fetch_some_data


with betamax.Betamax.configure() as config:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    config.cassette_library_dir = os.path.join(current_dir, 'cassettes')


@patch('rock.dal.requests.Session')
def test_fetch_some_data(requests_mock):
    requests_mock.return_value.get.return_value = 'Metalica'
    test_url = 'http://cookies.me/eat'
    results = fetch_some_data(test_url)
    assert 'Metalica' == results
    requests_mock.return_value.get.assert_called_once_with(test_url)


@patch('rock.dal.requests.Session')
def test_fetch_some_data_conn_error(requests_mock):
    requests_mock.return_value.get.side_effect = ConnectionError('boom')
    test_url = 'http://cookies.me/eat'
    results = fetch_some_data(test_url)
    assert results is None
    requests_mock.return_value.get.assert_called_once_with(test_url)


@patch('rock.dal.requests')
def test_fetch_some_data_betamax(requests_mock):
    session = requests.Session()
    requests_mock.Session.return_value = session
    with Betamax(session).use_cassette('fetch_some_data'):
        results = fetch_some_data('https://jsonplaceholder.typicode.com/posts')
    assert 'body' in results.text
    assert 1 == results.json()[0]['userId']
