from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e9e0a536bfa9e4ce1e4c1a56'

from downloader import routes