from flask import (Flask, g, render_template, flash, url_for, redirect)
from flask_login import LoginManager, login_user, login_required, current_user,logout_user
from flask_bcrypt import check_password_hash
import models
import forms

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key =  '56d4asdw98q4dqwdcw8rer8h9hgj8khjk871;.432$"#&%$/(/)/&%$ER'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:    
        return None

@app.before_request
def before_request():
    g.db = models.db
    if g.db.is_closed():
        g.db.connect()
        g.user = current_user

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
            password = form.password.data
        )
        return redirect(url_for('/'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Vaya! parece que no coincide", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Haz iniciado sesión correctamente', 'success')
                return redirect(url_for('index'))
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/new_post', methods=('GET', 'POST'))
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(),content = form.content.data.strip())
        flash("Mensaje posteado","success")
        return redirect(url_for('index'))
    return render_template('post.html', form=form)


@app.route('/')
def index():
    stream = models.Post.select().limit(100)
    return render_template("stream.html", stream=stream)

@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    template = 'stream.html'
    if username and username != current_user.username:
        user = models.User.select().where(models.User.username**username).get()
        stream = user.post.limit(100)
    else:
        stream = current_user.get_stream().limit(100)
        user = current_user

    if username:
        template = 'user_stream.html'
    
    return render_template(template, stream=stream, user=user)

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)

