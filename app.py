import os

from flask import Flask

from extensions import mongo, scheduler
from api.v1.routes import api_v1
from jobs.config import Config
from jobs import tasks
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api_v1)

CORS(app)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo.init_app(app)

app.config.from_object(Config())

scheduler.init_app(app)
scheduler.start()

tasks.init()

if __name__ == '__main__':
    app.run(debug=True)
