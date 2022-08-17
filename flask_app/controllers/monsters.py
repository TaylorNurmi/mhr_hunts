from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.monster import Monster
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/monsters')
def allMonsters():
    monsters = Monster.get_monsties()
    return render_template("monsters.html", monsters = monsters)

@app.route('/monster/<int:id>')
def getMonster(id):
    data = {
        "id" : id
    }
    monster = Monster.get_monstie(data)
    hunts = User.get_all_hunt_info()
    return render_template("monsterinfo.html", monster = monster, hunts = hunts)