from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9e0a536bfa9e4ce1e4c1a56'
socketio = SocketIO(app)

from downloader import routes
