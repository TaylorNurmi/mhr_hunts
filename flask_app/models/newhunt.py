from ssl import create_default_context
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import monster
from flask_app.models import user
from flask_app.models import newhunt
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Hunt:

    def __init__(self, data):
        self.id = data['id']
        self.hunt_minutes = data['hunt_minutes']
        self.hunt_seconds = data['hunt_seconds']
        self.user_id = data['user_id']
        self.monster_id = data['monster_id']
        self.weapon_name = data['weapon_name']
        self.comments = data['comments']
        self.party_size = data['party_size']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.hunts = []

    @classmethod
    def save_hunt(cls, data):
        query = "INSERT INTO hunts ( hunt_minutes, hunt_seconds, user_id, monster_id, weapon_name, comments, party_size ) VALUES (%(hunt_minutes)s, %(hunt_seconds)s, %(user_id)s, %(monster_id)s, %(weapon_name)s, %(comments)s, %(party_size)s);"
        return connectToMySQL("mhr_hunts").query_db(query, data)

    @classmethod
    def get_newhunt_by_maxid(cls):
        query = "SELECT MAX(id) from hunts"
        return connectToMySQL("mhr_hunts").query_db(query)

    @classmethod
    def get_all_hunts(cls):
        query = "SELECT * from hunts"
        return connectToMySQL("mhr_hunts").query_db(query)

    @classmethod
    def user_hunts_with_weapons(cls, data):
        query = "SELECT * from hunts WHERE user_id = %(id)s"
        results = connectToMySQL("mhr_hunts").query_db(query, data)
        weapon_counts = []
        GS = 0
        LS = 0
        SS = 0
        DB = 0
        L = 0
        GL = 0
        H = 0
        HH = 0
        SA = 0
        CB = 0
        IG = 0
        LB = 0
        HB = 0
        B = 0
        for row in results:
            if row['weapon_name'] == "Great Sword":
                GS += 1
            if row['weapon_name'] == "Long Sword":
                LS += 1
            if row['weapon_name'] == "Sword & Shield":
                SS += 1
            if row['weapon_name'] == "Duel Blades":
                DB += 1
            if row['weapon_name'] == "Lance":
                L += 1
            if row['weapon_name'] == "Gunlance":
                GL += 1
            if row['weapon_name'] == "Hammer":
                H += 1
            if row['weapon_name'] == "Hunting Horn":
                HH += 1
            if row['weapon_name'] == "Switch Axe":
                SA += 1
            if row['weapon_name'] == "Charge Blade":
                CB += 1
            if row['weapon_name'] == "Insect Glaive":
                IG += 1
            if row['weapon_name'] == "Light Bowgun":
                LB += 1
            if row['weapon_name'] == "Heavy Bowgun":
                HB += 1
            if row['weapon_name'] == "Bow":
                B += 1
        weapon_counts.append("Great Sword" + " " + str(GS))
        weapon_counts.append("Long Sword" + " " + str(LS))
        weapon_counts.append("Sword & Shield" + " " + str(SS))
        weapon_counts.append("Duel Blades" + " " + str(DB))
        weapon_counts.append("Lance" + " " + str(L))
        weapon_counts.append("Gunlance" + " " + str(GL))
        weapon_counts.append("Hammer" + " " + str(H))
        weapon_counts.append("Hunting Horn" + " " + str(HH))
        weapon_counts.append("Switch Axe" + " " + str(SA))
        weapon_counts.append("Charge Blade" + " " + str(CB))
        weapon_counts.append("Insect Glaive" + " " + str(IG))
        weapon_counts.append("Light Bowgun" + " " + str(LB))
        weapon_counts.append("Heavy Bowgun" + " " + str(HB))
        weapon_counts.append("Bow" + " " + str(B))
        return weapon_counts


    @classmethod
    def save_comment(cls, data):
        query = "INSERT INTO comments (user_id, hunt_id, content) VALUES (%(user_id)s, %(hunt_id)s, %(content)s);"
        return connectToMySQL("mhr_hunts").query_db(query, data)

    @classmethod
    def get_comments(cls):
        query = "SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id;"
        return connectToMySQL("mhr_hunts").query_db(query)

    @classmethod
    def like_hunt(cls, data):
        query = "INSERT INTO post_likes (hunt_id, user_id) VALUES (%(hunt_id)s, %(user_id)s);"
        return connectToMySQL("mhr_hunts").query_db(query, data)

    @classmethod
    def get_hunt_likes(cls):
        query = "SELECT * FROM post_likes"
        return connectToMySQL("mhr_hunts").query_db(query)


    @staticmethod
    def validate_hunt( data ):
        is_valid = True
        if int(data['hunt_minutes']) > 60 or int(data['hunt_minutes']) < 0: 
            flash("Invalid Hunt Time!")
            is_valid = False
        if int(data['hunt_seconds']) > 60 or int(data['hunt_seconds']) < 0: 
            flash("Invalid Hunt Time!")
            is_valid = False
        if data['weapon_name'] == "Weapon Type":
            flash("You must Choose a weapon!")
        return is_valid
