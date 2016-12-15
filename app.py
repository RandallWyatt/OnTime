from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask.ext.login import LoginManager, login_user, UserMixin, login_required, logout_user
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:thisroot@localhost/ToDo'

app.config['SECRET_KEY'] = 'kaexplode'

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    tasks = db.relationship('Task', backref='user', lazy='dynamic')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    info = db.Column(db.String(200))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Your session has expired, login again.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route('/')
def main():
    style_link = 'styles'
    if 'color' in session:
        color = session['color']
        style_link = '/static/' + color + '.css'
    return render_template('index.html', styles=style_link)


@app.route('/color/<color>')
def change_color(color):
    session['color'] = color
    return redirect(url_for('main'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if 'email' in request.form:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user, remember=True)
            return redirect(url_for('main'))
        else:
            flash('Incorrect username and/or password!!!!!!!!!')
    return render_template('login.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('main'))
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out, login again.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()


