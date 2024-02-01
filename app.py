import sqlite3

from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from requests_html import HTML
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    intro = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.id}>'


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении произошла ошибка'
    else:
        return render_template('create-article.html')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<{self.login}:{self.id}>'


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if request.method == 'POST':
        if email and password:
            user = db.session.query(User).filter(User.email == email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(url_for('home.html'))
            else:
                return 'Неверное имя пользователя или пароль'
        else:
            return 'Пожалуйста, заполните все поля'
    return render_template('login.html')


@app.route('/registrate', methods=['POST', 'GET'])
def registrate():
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (email or password or password2):
            return 'Пожалуйста, заполните все поля'
        elif password != password2:
            return 'Пароли разные'
        else:
            result = db.session.query(User).filter(User.email == email).all()
            if not result:
                hash_password = generate_password_hash(password)
                new_user = User(email=email, password=hash_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                return 'Такой пользователь есть'

    return render_template('registrate.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
