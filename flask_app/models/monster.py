from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import newhunt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Monster:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.picture = data['picture']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_monsties(cls):
        query = "SELECT * FROM monsters;"
        results = connectToMySQL('mhr_hunts').query_db(query)
        monsters = []
        for monster in results:
            monsters.append( cls(monster) )
        return monsters

    @classmethod
    def get_monstie(cls, data):
        query = "SELECT * FROM monsters where id = %(id)s;"
        results = connectToMySQL('mhr_hunts').query_db(query, data)
        return results[0]

    