from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key= "b'\xb2<\xb0\xdc\xad\x12K\x85\xffj\xe7\x91\x8d\x95\x03Q\x9e\x98\xec.\xdb\x1bk'"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_BINDS'] = {'posts':'sqlite:///posts.db',
                                   'users' : 'sqlite:///users.db'}

db=SQLAlchemy(app)

#Main database
class main(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#Users database
class users(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(300))
    name = db.Column(db.String(300))
    number = db.Column(db.String(300))

    def __init__(self, username, email, name, number):
        self.username = username
        self.email = email
        self.name = name
        self.number = number

#Posts database
class posts(db.Model):
    __bind_key__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date_posted = db.Column(db.String(100))
    author = db.Column(db.String(100))
    content = db.Column(db.Text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts/')
def posts():
    return render_template('posts.html')

@app.route('/manageUsers/')
def manageUsers():
    userData = users.query.all()

    return render_template('manageUsers.html', user = userData)

@app.route('/manageUsers/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        name = request.form['name']
        number = request.form['number']

        newUserdb = users(username, email, name, number)
        db.session.add(newUserdb)
        db.session.commit()

        flash(username + " was created successfully!")

        return redirect(url_for('manageUsers'))

@app.route('/manageUsers/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        data = users.query.get(request.form.get('id'))
        data.username = request.form['username']
        data.name = request.form['name']
        data.email = request.form['email']
        data.number = request.form['number']
        db.session.commit()

        flash(data.username + " edited successfully!")

        return redirect(url_for('manageUsers'))

@app.route('/manageUsers/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    data = users.query.get(id)
    db.session.delete(data)
    db.session.commit()

    flash(data.username + " was deleted successfully!")
        
    return redirect(url_for('manageUsers'))



if __name__ == "__main__":
    app.run(debug=True)