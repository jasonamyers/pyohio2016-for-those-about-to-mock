import requests
from requests import ConnectionError


def process_results(results):
    if results.status_code == 404:
        return {'message': 'Rock Not found!'}
    elif results.status_code == 500:
        return {'message': 'Rock Imploded!'}
    elif results.status_code == 200:
        return results.json()
    else:
        raise ValueError('SHARON!')


def process_file(filename):
    lines = []
    with open(filename, 'rw') as proc_file:
        for line in proc_file:
            lines.append(line.strip('\n'))
    return lines


def fetch_some_data(url):
    session = requests.Session()
    results = None
    try:
        results = session.get(url)
    except ConnectionError as exc_info:
        print(str(exc_info))
    return results


def str_to_int(value):
    return int(value)


def string_adder(value):
    numbers = value.split(',')
    clean_numbers = []
    for number in numbers:
        clean_numbers.append(str_to_int(number))
    return sum(clean_numbers)
