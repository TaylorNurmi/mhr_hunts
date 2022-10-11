from flask import Flask, render_template, session, request, redirect, url_for
from flask_app.models.monster import Monster
from flask_app import app
from flask_app.models.newhunt import Hunt
from flask_app.config.mysqlconnection import connectToMySQL
import pymysql



@app.route('/newhunt/<int:id>')
def addHunt(id):
    data = {
        "id" : id
    }
    temp = Monster.get_monstie(data)
    session['monster_id'] = temp['id']
    print (session['monster_id'])
    monster = Monster.get_monstie(data)
    print (monster)
    return render_template("newhunt.html", monster = monster)

@app.route('/addhunt', methods = ['Post'])
def post_hunt():
    data = {
        "hunt_minutes": request.form['hunt_minutes'],
        "hunt_seconds": request.form['hunt_seconds'],
        "user_id": session['user_id'],
        "monster_id": session['monster_id'],
        "weapon_name": request.form['weapon_name'],
        "comments": request.form['comments'],
        "party_size": request.form['party_size']
    }
    if not Hunt.validate_hunt(request.form):
        return redirect(url_for('addHunt', id = data['monster_id']))
    Hunt.save_hunt(data)
    return redirect("/home")

@app.route('/addcomment', methods = ['Post'])
def post_comment():
    data = {
        "user_id": session['user_id'],
        "hunt_id": request.form['hunt_id'],
        "content": request.form['comment_text']
    }
    Hunt.save_comment(data)
    return redirect("/home")


@app.route('/add_like', methods = ["POST","GET"])
def like_hunt():
    data = { 
        "hunt_id" : request.form.get("hunt_id"),
        "user_id": session["user_id"]
        }
    Hunt.like_hunt(data)
    return redirect("/home")

@app.route("/delete/<int:id>", methods = ["post"])
def delete(id):
    data = {
        "id": id
    }
    Hunt.delete_likes(data)
    Hunt.delete_comments(data)
    Hunt.delete(data)
    return redirect("/home")

@app.route('/edit/<int:id>')
def edit(id):
    data = {
        "id": id
    }
    hunt = Hunt.get_one_hunt(data)
    session['hunt_id'] = id
    return render_template("edithunt.html", hunt = hunt[0])


@app.route('/updatehunt', methods = ["post"])
def update():
    data = {
        "id": session['hunt_id'],
        "hunt_minutes": request.form['hunt_minutes'],
        "hunt_seconds": request.form['hunt_seconds'],
        "weapon_name": request.form['weapon_name'],
        "comments": request.form['comments'],
        "party_size": request.form['party_size']
    }
    Hunt.update(data)
    return redirect("/home")