from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user
from flask import flash


class Pony:

    def __init__( self , data ):
        self.id = data["id"]
        self.name = data["name"]
        self.location_made = data["location_made"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = user.User.get_by_id({"id": data["user_id"]})



# Create
    @classmethod
    def save(cls,data):
        query = "INSERT INTO ponys (name, location_made, comment, user_id) VALUES (%(name)s, %(location_made)s, %(comment)s, %(user_id)s);"
        return connectToMySQL("mlp_schema").query_db(query,data)


# READ
    # read many
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ponys;"
        results = connectToMySQL("mlp_schema").query_db(query)
        ponys = []
        for row in results:
            ponys.append(cls(row))
        return ponys


# read one
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM ponys WHERE id = %(id)s;"
        results = connectToMySQL("mlp_schema").query_db(query, data) 
        return cls(results[0])


# UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE ponys SET name=%(name)s, location_made=%(location_made)s, comment=%(comment)s, updated_at = Now() WHERE id = %(id)s;"
        return connectToMySQL("mlp_schema").query_db(query,data)


# DELETE
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM ponys WHERE id = %(id)s;"
        return connectToMySQL("mlp_schema").query_db(query,data)


# VALIDATE
    @staticmethod
    def validate_pony(pony):
        is_valid = True
        if len(pony["name"]) < 5:
            flash("name must be at least 5 characters.", "pony")
            is_valid = False
        if len(pony["location_made"]) < 2:
            flash("Location must be at least 2 characters.", "pony")
            is_valid = False
        if len(pony["comment"]) >= 100:
            flash("Reason must be a max of 100 characters.", "pony")
            is_valid = False
        return is_valid