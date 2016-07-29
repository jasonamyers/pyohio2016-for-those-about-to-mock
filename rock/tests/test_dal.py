import os

import betamax
from betamax import Betamax
from mock import patch, call
import pytest
import requests
from requests import ConnectionError

from rock.dal import fetch_some_data, string_adder, str_to_int


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


@patch('rock.dal.str_to_int')
def test_string_adder(s2i_mock):
    s2i_mock.side_effect = [2, 3]
    result = string_adder("2,3")
    assert result == 5
    assert s2i_mock.mock_calls == [call("2"), call("3")]


@pytest.mark.parametrize("test_input,expected", [("3", 3), ("-1", -1)])
def test_str_to_int(test_input, expected):
    assert str_to_int(test_input) == expected
