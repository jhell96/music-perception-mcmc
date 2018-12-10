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
    js_file = 'scripts.js'
    return send_file(js_file)

@app.route ('/style.css')
def css():
    cs_file = 'style.css'
    return send_file(cs_file)

@app.route('/resources/<path:path>')
def resources(path):
    return send_from_directory('resources/', path)

@app.route('/post_data', methods=['GET', 'POST'])
def store_tests():
    test1 = request.values.get('test1')
    test2 = request.values.get('test2')
    test3 = request.values.get('test3')
    test4 = request.values.get('test4')
    test5 = request.values.get('test5')

    print (test1)
    print (test2)
    print (test3)
    print (test4)
    print (test5)



    return jsonify({
        'message':'ok'
        })





if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)
