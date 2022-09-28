from flask import Flask
import OthelloAB

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

app.run(debug = True)
