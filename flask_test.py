import flask

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/")
def get_main_page():
    return flask.render_template('ScenicComps.html')

if __name__ == "__main__":
    app.run()