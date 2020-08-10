from flask import Flask
from flask import request 
from flask import render_template

app = Flask(__name__)

@app.route('/<name>')
def index(name="Daniel"):
    return render_template("add.html",
    name=name)

@app.route('/welcome')
def welcome():
    context = {"message": "hola", "title":"Welcome"}
    return render_template("welcome.html", **context)

@app.route('/example')
def example(id=0):
    id = request.args.get('id')
    return "Current ID: {}".format(id)


@app.route('/q')   
@app.route('/q/<int:id>')
def query(id="1"):
    id = request.args.get('id',id)
    return "Current ID: {}".format(id)


app.run(debug=True, port=8000, host='127.0.0.1')


