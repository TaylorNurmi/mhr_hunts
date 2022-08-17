from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.newhunt import Hunt
import base64
import os
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def displayLanding():
    return render_template("login.html")

@app.route('/newhunter')
def newhunter():
    return render_template("signup.html")

@app.route('/home')
def userHome():
    data = {
        "id" : session['user_id']
    }
    users = User.get_user(data)
    pic = users['pfp']
    print (pic)
    weapons = Hunt.user_hunts_with_weapons(data)
    hunts = User.get_all__recent_hunt_info()
    all_hunts = User.get_all_hunt_info()
    all_users = User.get_all()
    hunt_comments = Hunt.get_comments()
    likes = Hunt.get_hunt_likes()
    return render_template("user.html", users = users, pic = pic, weapons = weapons, hunts = hunts, all_users = all_users, hunt_comments = hunt_comments, likes = likes)

@app.route('/user/<int:id>')
def otherHunters(id):
    data = {
        "id" : id
    }
    users = User.get_user(data)
    pic = users['pfp']
    weapons = Hunt.user_hunts_with_weapons(data)
    hunts = User.get_all__user_hunt_info(data)
    all_users = User.get_all()
    hunt_comments = Hunt.get_comments()
    likes = Hunt.get_hunt_likes()
    return render_template("otherusers.html", users = users, pic = pic, weapons = weapons, hunts = hunts, all_users = all_users, hunt_comments = hunt_comments, likes = likes)

@app.route('/addphoto', methods = ['Post'])
def addpfp():
    if request.method == 'POST':
        f = request.files['pfp']
        filename = (secure_filename(f.filename))
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
        relative_path = os.path.relpath(path)
        relative_path = list(relative_path)
        for i in range(len(relative_path)):
            if relative_path[i] == '\'' or relative_path[i] == '\\':
                relative_path[i] = "/"
            elif i <= 8:
                relative_path[i] = ""
        new_path = ""
        new_path = new_path.join(relative_path)
        print (new_path)
        data = {
            "pfp": new_path,
            "id": session['user_id']
        }
        User.save_photo(data)
        return redirect ('/home')


@app.route('/signup', methods = ['Post'])
def signup():
    data = { 
        "email" : request.form["email"] 
        }
    user_exists = User.get_user_by_email(data)
    if user_exists:
        flash("email already in use")
        return redirect("/newhunter")
    if not User.validate_signup(request.form):
        return redirect('/newhunter')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "email": request.form["email"],
            "hunter_name": request.form["hunter_name"],
            "password": pw_hash,
            "confirm": request.form["confirm"]
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        session['user_name'] = request.form["hunter_name"]
    return redirect("/home")


@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user_exists = User.get_user_by_email(data)
    if not user_exists:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_exists['password'], request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_exists['id']
    session['user_name'] = user_exists['hunter_name']
    return redirect("/home")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')