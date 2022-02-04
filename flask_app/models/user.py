from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import pony

class User:

    def __init__( self , data ):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data['password']
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.ponys = []


# CREATE
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("mlp_schema").query_db(query,data)


# READ - not needed
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("mlp_schema").query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users


# read one
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("mlp_schema").query_db(query,data)
        if not results:
            return False
        return cls(results[0])


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("mlp_schema").query_db(query,data)
        if not results:
            return False
        return cls(results[0])


    @classmethod
    def get_one_with_ponys( cls , data ):
        query = "SELECT * FROM users LEFT JOIN ponys ON users.id = ponys.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL("mlp_schema").query_db( query, data )
        user = cls( results[0] )
        for row_from_db in results:
            pony_data = {
                "user_id" : row_from_db["user_id"],
                "id" : row_from_db["ponys.id"],
                "name" : row_from_db["name"],
                "location_made" : row_from_db["location_made"],
                "comment" : row_from_db["comment"],
                "created_at" : row_from_db["ponys.created_at"],
                "updated_at" : row_from_db["ponys.updated_at"]
            }
            user.ponys.append(pony.Pony(pony_data))
        return user


# VALIDATE
    @staticmethod
    def validate_register(user):
        is_valid = True
        results = User.get_by_email(user)
        if len(user["first_name"]) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid= False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least 2 characters.","register")
            is_valid= False
        if results:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email!","register")
            is_valid=False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False
        if not any(char.isupper() for char in user["password"]):
            flash("Password should have at least one uppercase letter.","register")
            is_valid = False
        if not any(char.islower() for char in user["password"]):
            flash("Password should have at least one lowercase letter.","register")
            is_valid = False
        if not any(char.isnumeric() for char in user["password"]):
            flash("Password should have at least one number.","register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash("Passwords don't match.")
            is_valid = False
        return is_valid