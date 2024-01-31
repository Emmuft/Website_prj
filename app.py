
import sqlite3

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from requests_html import HTML

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
        return '<Article %r>' % self.id


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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User(email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении произошла ошибка'

    else:
        return render_template('login.html')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/registrate', methods=['POST', 'GET'])
def registrate():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        result = db.session.query(User).filter(User.email == email).all()
        if not result:
            if password == password2:
                user = User(email=email, password=password)
                try:
                    db.add(user)
                    db.session.commit()
                    return redirect('/home')
                except:
                    return 'При добавлении произошла ошибка'
            else:
                return 'Пароли не совпадают'
        else:
            return 'Пользователь с такой почтой существует'

    else:
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
