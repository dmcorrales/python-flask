from flask import Flask
from flask import request 

app = Flask(__name__)

@app.route('/')
def index(id=0):
    id = request.args.get('id')
    return "Current ID: {}".format(id)


@app.route('/q')   
@app.route('/q/<id>')
def query(id="1"):
    id = request.args.get('id',id)
    return "Current ID: {}".format(id)


app.run(debug=True, port=8000, host='127.0.0.1')


