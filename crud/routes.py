from flask import Flask, render_template, request, redirect, url_for, flash
from crud import db, app, bcrypt
from crud.models import postdb, users, main, loginForm, postForm, editUserForm


@app.route('/')
def index():
    login = loginForm()
    return render_template('index.html', loginform=login)


@app.route('/posts/',)
def posts():
    postData = postdb.query.all()
    postFormInput = postForm()
    return render_template('posts.html', postData=postData, post=postFormInput)


@app.route('/login/', methods=['POST'])
def login():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        register = loginForm()
        username = register.username.data
        email = register.email.data
        name = register.name.data
        hashed_password = bcrypt.generate_password_hash(register.password.data).decode('utf-8')
        password = hashed_password
        number = register.phone.data

        newUserdb = users(username, email, name, number, password)
        db.session.add(newUserdb)
        db.session.commit()

        flash('You have successfully registered!')

        return redirect(url_for('index'))


@app.route('/posts/new', methods=['POST'])
def new():
    if request.method == 'POST':
        title = postForm.title.data
        author = postForm.author.data
        content = postForm.content.data

        newPostdb = postdb(title, author, content)
        db.session.add(newPostdb)
        db.session.commit()

        flash('"' + title + '"' + " was posted successfully!")

        return redirect(url_for('posts'))


@app.route('/posts/editPost', methods=['GET', 'POST'])
def editPost():
    if request.method == 'POST':
        data = postdb.query.get(request.form.get('id'))
        data.title = request.form['title']
        data.author = request.form['author']
        data.content = request.form['content']
        db.session.commit()

        flash('"' + data.title + '"' + " edited successfully!")

        return redirect(url_for('posts'))


@app.route('/posts/deletepost/<id>/', methods=['GET', 'POST'])
def deletepost(id):
    data = postdb.query.get(id)
    db.session.delete(data)
    db.session.commit()

    flash('"' + data.title + '"' + " was deleted successfully!")

    return redirect(url_for('posts'))


@app.route('/manageUsers/')
def manageUsers():
    login = loginForm()
    userData = users.query.all()
    edit = editUserForm()

    return render_template('manageUsers.html', user=userData, loginform=login, editUser=edit)


@app.route('/manageUsers/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        register = loginForm()
        username = register.username.data
        email = register.email.data
        name = register.name.data
        hashed_password = bcrypt.generate_password_hash(register.password.data).decode('utf-8')
        password = hashed_password
        number = register.phone.data

        newUserdb = users(username, email, name, number, password)
        db.session.add(newUserdb)
        db.session.commit()

        flash('"' + username + '"' + " was created successfully!")

        return redirect(url_for('manageUsers'))


@app.route('/manageUsers/edit/', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        edit = editUserForm()
        data = users.query.get(edit.id.data)
        data.username = edit.username.data
        data.name = edit.name.data
        data.email = edit.email.data
        data.number = edit.phone.data
        db.session.commit()

        flash('"' + data.username + '"' + " edited successfully!")

        return redirect(url_for('manageUsers'))


@app.route('/manageUsers/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    data = users.query.get(id)
    db.session.delete(data)
    db.session.commit()

    flash('"' + data.username + '"' + " was deleted successfully!")

    return redirect(url_for('manageUsers'))
