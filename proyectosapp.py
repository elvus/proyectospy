from flask import Flask, Response, render_template
from flask_cors import CORS
from bson.json_util import dumps
from requests.api import request

from proyectos import connection
import urllib3

app = Flask(__name__, static_folder='./build', static_url_path='/')
cors = CORS(app, resources={r"/api/*": {"origins":"*"}})

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/all")
def api_root():
    db=connection()
    response=dumps(db.proyectos.find())
    return Response(response=response, status=200, mimetype='application/json')


if __name__=="__main__":
        app.run()
        