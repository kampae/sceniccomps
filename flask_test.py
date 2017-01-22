import flask
import json
from flask import Flask, jsonify, render_template
from flask.ext.googlemaps import GoogleMaps
from flask_googlemaps import Map

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

app.config['GOOGLEMAPS_KEY'] = 'AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4'
GoogleMaps(app, key='AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4')

@app.route("/")
def get_main_page():
    return flask.render_template('ScenicComps.html')

@app.route("/<inputs>/")
def second_page(inputs):
    return json.dumps(inputs)

@app.route("/<start>/<end>/<time>/<scenery>/")
def route_display(start, end, time, scenery):
    # code here to generate route
    # pass coordinates to route.js
    
    return flask.render_template('route.html')

@app.route('/map/')
def view_map():
    mymap = Map(
        identifier="fullmap",
        varname="mymap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat = 37.4419,
        lng = -122.1419,
        markers=[(37.4419, -122.1419)]
    )
    
    return flask.render_template('map.html', mymap=mymap)
    #return jsonify(mymap.as_json())

if __name__ == "__main__":
    
    app.run(host='localhost', port=5000, debug=True, use_reloader=True)