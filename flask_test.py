import flask
import json
from flask import Flask, jsonify, render_template, request, session
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
import distance_matrix
import check_user_input

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'F33459345**&4D';
app.config['GOOGLEMAPS_KEY'] = 'AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4'
GoogleMaps(app, key='AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4')

@app.route("/")
def get_main_page():
    #return flask.render_template('ScenicComps.html')
    return flask.render_template('ScenicTiles.html', badInput=0, start="", end="", hours=0, minutes=0, scenicChoice="Select Scenery")


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
    
    startpoint_url = startpoint.replace(" ", "+")
    endpoint_url = endpoint.replace(" ", "+")
#    scenery_caps = scenery[0].upper() + scenery[1:]
#    print(scenery_caps)
    
    # This code calls check_user_input module and makes sure time given is at least as much as it takes
        # to get from start to end directly
    max_time = (int(hours)*60 + int(minutes))*60
    start_valid = check_user_input.check_address(startpoint_url)
    if not start_valid:
        return flask.render_template('ScenicTiles.html', badInput=1, start=startpoint, end=endpoint, hours=hours, minutes=minutes, scenicChoice=scenery)
    
    end_valid = check_user_input.check_address(endpoint_url)
    if not end_valid:
        return flask.render_template('ScenicTiles.html', badInput=2, start=startpoint, end=endpoint, hours=hours, minutes=minutes, scenicChoice=scenery)
    
    time_valid = check_user_input.check_max_time(max_time, startpoint_url, endpoint_url)
    if not time_valid:
        return flask.render_template('ScenicTiles.html', badInput=3, start=startpoint, end=endpoint, hours=hours, minutes=minutes, scenicChoice=scenery)
    #print(startpoint, endpoint)
    #waypoints = distance_matrix.get_waypoints("2201+E+Newton+St,+Seattle,WA", "3324+NE+21st+Ave+Portland,OR+97212", "non-scenic", "22", "2")
    waypoints = distance_matrix.get_waypoints(startpoint_url, endpoint_url, scenery, hours, minutes)
    print("WAYPOINTS: ", waypoints)
    return flask.render_template('route.html', waypoints = waypoints)
#    
    
def test(startpoint):
    return '47.626925'

if __name__ == "__main__":
    
    app.run(host='localhost', port=5000, debug=True, use_reloader=True)