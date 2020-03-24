from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


async_mode = None
app = Flask(__name__)
app.config.from_pyfile('../config.cfg')
socketio = SocketIO(app)
db = SQLAlchemy(app)

import vehicle_tracker.model  # NOQA
import vehicle_tracker.service  # NOQA
