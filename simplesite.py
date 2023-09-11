import flask
from flask_bootstrap import Bootstrap
from flask import Flask, request, redirect, abort, render_template, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#для тестирования
user_dict = {"mary sue": "123", "admin": "123", "wanderer": "123"}
chat = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'example key'
bootstrap = Bootstrap(app)


def load_user(name: str):
    if name in user_dict.values():
        return name
    return None


class Register(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class Login(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class Message(FlaskForm):
    message = StringField('>>', validators=[DataRequired()])
    submit = SubmitField('Отправить')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    user_agent = request.headers.get('User-Agent')
    t = flask.current_app.name
    # return '<h1>Bad Request</h1>', 400
    username = None
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        if username in user_dict.keys():
            return render_template('register.html', form=form, name=username, taken=True, session_name=session['name'])
        else:
            user_dict[username] = password
            session['name'] = username
            return redirect(url_for('get_user', name=username, _external=True))
    return render_template('register.html', form=form, name=username, taken=False, session_name=session['name'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    username = None
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        if username not in user_dict.keys():
            return render_template('login.html', form=form, name=None, not_found=True, wrong_pass=False,
                                   session_name=session['name'])
        else:
            if password != user_dict[username]:
                return render_template('login.html', form=form, name=None, not_found=False, wrong_pass=True,
                                       session_name=session['name'])
            session['name'] = username
            return redirect(url_for('get_user', name=username, _external=True, session_name=session['name']))
    return render_template('login.html', form=form, name=username, not_found=False, wrong_pass=False,
                           session_name=session['name'])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Message()
    if form.validate_on_submit():
        chat.append((session['name'], form.message.data))
    return render_template('home.html', session_name=session['name'], chat=chat, form=form)


@app.route('/out', methods=['GET', 'POST'])
def out():
    form = Message()
    session['name'] = None
    return redirect(url_for('index', _external=True, session_name=session['name'], chat=chat, form=form))


# return '<p>Your browser is {}</p> <p>{}</p>'.format(user_agent, t)


@app.route('/user/<name>')
def get_user(name):
    if name not in user_dict.keys():
        abort(404)
    return render_template('./user1.html', name=name, users=user_dict, session_name=session['name'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
