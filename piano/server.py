#!/usr/bin/python3

from flask import Flask, request, jsonify, send_file, send_from_directory
import random

app = Flask(__name__)


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
    skill_level = request.values.get('skill-level')

    test1_plays = request.values.get('test1-plays')
    test1 = request.values.get('test1')

    test2_plays = request.values.get('test2-plays')
    test2 = request.values.get('test2')

    test3_plays = request.values.get('test3-plays')
    test3 = request.values.get('test3')

    test4_plays = request.values.get('test4-plays')
    test4 = request.values.get('test4')

    test5_plays = request.values.get('test5-plays')
    test5 = request.values.get('test5')

    if (skill_level and 
        test1 and test1_plays and 
        test2 and test2_plays and 
        test3 and test3_plays and 
        test4 and test4_plays and
        test5 and test5_plays):

        with open('data/raw/trials.txt', 'a') as f:
            f.write('\n')
            f.write(skill_level)
            f.write('\n')
            f.write(test1)
            f.write('\n')
            f.write(test1_plays)
            f.write('\n')
            f.write(test2)
            f.write('\n')
            f.write(test2_plays)
            f.write('\n')
            f.write(test3)
            f.write('\n')
            f.write(test3_plays)
            f.write('\n')
            f.write(test4)
            f.write('\n')
            f.write(test4_plays)
            f.write('\n')
            f.write(test5)
            f.write('\n')
            f.write(test5_plays)
            f.write('\n')
            f.write("-"*100)


    return jsonify({
        'message':'ok'
        })


if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)
