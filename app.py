import os

from flask import Flask, session

from extensions import mongo, scheduler
from api.v1.routes import api_v1
from api.oauth.google_oauth2 import google_oauth2
from jobs.config import Config
from jobs import tasks
from flask_cors import CORS

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY')

app.register_blueprint(api_v1)
app.register_blueprint(google_oauth2)

CORS(app, origins=['http://localhost:5000'], resources=r'/api/*')
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo.init_app(app)

app.config.from_object(Config())

scheduler.init_app(app)
scheduler.start()

tasks.init()

if __name__ == '__main__':
    app.run(debug=True)
