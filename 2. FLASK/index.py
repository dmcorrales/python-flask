from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Index page"

app.run(debug=True, port=8000, host='127.0.0.1')


