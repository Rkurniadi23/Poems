from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "poems_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.confirm_pw=None


# CREATE USER..................
    @classmethod
    def save(cls, data):
        query="""
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)


# GET USER..............
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, user_id):
        query = " SELECT * FROM users WHERE id = %(id)s;"
        data = {'id':user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    # VALIDATIONS:
    @staticmethod
    def validate_user(user):
        is_valid = True
  
    
        if len(user["first_name"]) == 0:
            flash("First Name is rquired.")
            is_valid = False
        if len(user["last_name"]) == 0:
            flash("Last Name is required.")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last Name must be at least 2 characteres.")
            is_valid = False
        if len(user["first_name"]) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
      
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
 
        if len(user["password"]) == 0:
            flash("Password is required.")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characteres.")
            is_valid = False
        if len(user["confirm_pw"]) == 0:
            flash("Please confirm password.")
            is_valid = False
        if (user["confirm_pw"]) != (user["password"]):
            flash("Passwords do not match.")
            is_valid = False
        return is_valid