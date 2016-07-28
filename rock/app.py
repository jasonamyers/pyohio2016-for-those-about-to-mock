from flask import Flask, jsonify, Response

from dal import process_results, fetch_some_data

app = Flask(__name__)

rock_api_url = 'https://jsonplaceholder.typicode.com/posts'


def hello_world():
    return {'message': 'Hello World'}


@app.route('/hello/')
def api_hello_world():
    return jsonify(hello_world)


@app.route('/rock/')
def api_get_rock():
    results = fetch_some_data(rock_api_url)
    return build_result_response(results)


def build_result_response(results):
    processed = process_results(results)
    return jsonify(processed)

if __name__ == '__main__':
    app.run()
