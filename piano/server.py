#!/usr/bin/python3

from flask import Flask, request, jsonify, send_file, send_from_directory
import random

app = Flask(__name__)

help_queue = []
checkoff_queue = []


@app.route('/')
def index():
    index_file = 'index.html'
    return send_file(index_file)

@app.route('/test1.html')
def test1():
    return send_file('test1.html')

@app.route('/test2.html')
def test2():
    return send_file('test2.html')

@app.route('/test3.html')
def test3():
    return send_file('test3.html')

@app.route('/test4.html')
def test4():
    return send_file('test4.html')

@app.route('/test5.html')
def test5():
    return send_file('test5.html')

@app.route('/scripts.js')
def js():
    js_file = '/scripts.js'
    return send_file(js_file)

# @app.route ('/style.css')
# def css():
#     cs_file = '/style.css'
#     return send_file(cs_file)

@app.route('/resources/<path:path>')
def resources():
    return send_from_directory('/resources/', path)

@app.route('/post_data', methods=['GET', 'POST'])
def store_tests():
    if request.method == 'POST':
        for value in request.values:
            test_data = request.values[value]




if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)
