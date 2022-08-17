import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import monster
from flask_app.models import newhunt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:

    def __init__(self, data):
        self.id = data['id']
        self.pfp = data['pfp']
        self.hunter_name = data['hunter_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.hunt_list = []


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (hunter_name, email, password) VALUES (%(hunter_name)s, %(email)s, %(password)s);"
        return connectToMySQL("mhr_hunts").query_db(query, data)
    
    @classmethod
    def save_photo(cls,data):
        query = "UPDATE users SET pfp = %(pfp)s WHERE ID = %(id)s;"
        return connectToMySQL("mhr_hunts").query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("mhr_hunts").query_db(query, data)
        for row in results:
            return row

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users where id = %(id)s;"
        results = connectToMySQL('mhr_hunts').query_db(query, data)
        return results[0]

    @classmethod
    def get_all (cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('mhr_hunts').query_db(query)
        users = []
        for user in results:
            users.append( cls(user))
        return users

    @classmethod
    def get_all_hunt_info(cls):
        query = "SELECT * FROM users LEFT JOIN hunts ON hunts.user_id = users.id LEFT JOIN monsters ON hunts.monster_id = monsters.id WHERE hunts.id != 'null' ORDER BY hunts.id DESC;"
        results = connectToMySQL('mhr_hunts').query_db(query)
        hunt = []
        for row in results:
            hunt.append( row )
        return hunt

    @classmethod
    def get_all__recent_hunt_info(cls):
        query = "SELECT * FROM hunts LEFT JOIN users ON hunts.user_id = users.id LEFT JOIN monsters ON hunts.monster_id = monsters.id WHERE hunts.id != 'null' ORDER BY hunts.id DESC limit 10;"
        results = connectToMySQL('mhr_hunts').query_db(query)
        hunt = []
        for row in results:
            hunt.append( row )
        return hunt

    @classmethod
    def get_all__user_hunt_info(cls, data):
        query = "SELECT * FROM hunts LEFT JOIN users ON hunts.user_id = users.id LEFT JOIN monsters ON hunts.monster_id = monsters.id WHERE hunts.id != 'null' and hunts.user_id = %(id)s ORDER BY hunts.id DESC limit 10;"
        results = connectToMySQL('mhr_hunts').query_db(query, data)
        hunt = []
        for row in results:
            hunt.append( row )
        return hunt

    @staticmethod
    def validate_signup( data ):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['hunter_name']) < 2: 
            flash("First Name too short!")
            is_valid = False
        if data['confirm'] != data['password']:
            flash("Passwords DO NOT match")
            is_valid = False
        if len(data['password']) <= 8: 
            flash("Invalid Password!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_signin( data ):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['password']) < 8: 
            flash("Invalid Password!")
            is_valid = False
        return is_valid
