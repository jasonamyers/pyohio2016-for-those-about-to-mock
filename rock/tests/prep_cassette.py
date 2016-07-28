import os

import betamax
import requests

current_dir = os.path.abspath(os.path.dirname(__file__))
CASSETTE_LIBRARY_DIR = os.path.join(current_dir, 'cassettes')


def main():
    session = requests.Session()
    recorder = betamax.Betamax(
        session, cassette_library_dir=CASSETTE_LIBRARY_DIR
    )

    with recorder.use_cassette('fetch_some_data'):
        session.get('https://jsonplaceholder.typicode.com/posts')


if __name__ == '__main__':
    main()
