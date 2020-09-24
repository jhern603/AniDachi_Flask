from flask import Flask, render_template, request, redirect, url_for, flash
from crud import db, app, bcrypt
from crud.models import postdb, users, main
from crud.forms import register_form, post_form, edit_user_form, login_form
from flask_login import login_user


@app.route('/')
def index():
    register = register_form()
    login = login_form()
    return render_template('index.html', registerform=register, loginform=login)


# Forum Pages
@app.route('/posts/',)
def posts():
    post_data = postdb.query.all()
    post_form_input = post_form()
    return render_template('posts.html', postData=post_data, postForm=post_form_input)


@app.route('/posts/new', methods=['POST'])
def new():
    post = post_form()
    if request.method == 'POST':
        title = post.title.data
        author = post.author.data
        content = post.content.data

        new_postdb = postdb(title, author, content)
        db.session.add(new_postdb)
        db.session.commit()

        flash('"' + title + '"' + " was posted successfully!")

        return redirect(url_for('posts'))


@app.route('/posts/editPost', methods=['GET', 'POST'])
def editPost():
    post = post_form()
    if request.method == 'POST':
        data = postdb.query.get(post.id.data)
        data.title = post.title.data
        data.author = post.author.data
        data.content = post.content.data
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


# User Management pages
@app.route('/login', methods=['POST'])
def login():
    login = login_form()
    user = users.query.filter_by(username=login.username.data).first()
    if user and bcrypt.check_password_hash(user.password, login.password.data):
        #login_user(user, remember=login.remember.data)
        return redirect(url_for('manageUsers'))
    else:
        flash("Failed to log you in. Please try again.")
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    register = register_form()
    if register.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            register.password.data).decode('utf-8')
        password = hashed_password
        newUserdb = users(username=register.username.data, email=register.email.data,
                          name=register.name.data, number=register.phone.data, password=password)
        db.session.add(newUserdb)
        db.session.commit()
        flash('You have successfully registered!')

    return redirect(url_for('index'))


@app.route('/manageUsers/')
def manageUsers():
    login = register_form()
    userData = users.query.all()
    edit = edit_user_form()

    return render_template('manageUsers.html', user=userData, loginform=login, editUser=edit)


@app.route('/manageUsers/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        register = register_form()
        username = register.username.data
        email = register.email.data
        name = register.name.data
        hashed_password = bcrypt.generate_password_hash(
            register.password.data).decode('utf-8')
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
        edit = edit_user_form()
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
