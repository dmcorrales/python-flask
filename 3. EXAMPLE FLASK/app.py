from flask import (Flask, g, render_template, flash, url_for, redirect)
from flask_login import LoginManager
import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key =  '56d4asdw98q4dqwdcw8rer8h9hgj8khjk871;.432$"#&%$/(/)/&%$ER'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view

@login_manager
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:    
        return None

@app.before_request
def before_request():
    if not hasattr(g, 'db'):
        g.db = models.db
        g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/register', methods=('GET','POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('Fuiste registrado con éxito', 'success')
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.date
        )
        return redirect(url_for(''))

@app.route('/')
def index():
    return 'hey'

if __name__ == "__main__":
    models.initialize()
    models.User.create_user(
        username = 'asstag',
        email = 'dmcorrales@hotmail.com',
        password = ' calabaza',
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)

