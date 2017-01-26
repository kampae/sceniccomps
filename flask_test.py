import flask
import json
from flask import Flask, jsonify, render_template, request, session
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'F33459345**&4D';
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4'
GoogleMaps(app, key='AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4')

@app.route("/")
def get_main_page():
    return flask.render_template('ScenicComps.html')

@app.route("/<inputs>/")
def second_page(inputs):
    return json.dumps(inputs)

@app.route("/route/")    #<start>/<end>/<time>/<scenery>/")
def route_display(): #(start, end, time, scenery):
    # code here to generate route
    # pass coordinates to route.js 
#    if request.method == 'GET':
    return flask.render_template('route.html')

@app.route('/view_map', methods=['POST'])
def view_map():
    startpoint = request.form['startpoint']
    endpoint = request.form['endpoint']
    scenery = request.form['scenery']
    hours = request.form['hours']
    minutes = request.form['minutes']
    waypoints = [startpoint, "[47.619869, -119.459762]", "[47.646012, -119.358825]", endpoint]
    return flask.render_template('route.html', waypoints=waypoints, endpoint=endpoint)
    
    
def test(startpoint):
    return '47.626925'

if __name__ == "__main__":
    
    app.run(host='localhost', port=5000, debug=True, use_reloader=True)