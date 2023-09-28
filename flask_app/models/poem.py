from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Poem:
    DB = "poems_schema"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.author = data['author']
        self.genre=data['genre']
        self.poem_text=data['poem_text']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.user=None
    
    # Create Poems
    @classmethod
    def save(cls,data):

        query = """INSERT INTO poems (title, author, genre, poem_text, user_id) 
                VALUES (%(title)s,%(author)s,%(genre)s,%(poem_text)s,%(user_id)s);"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM poems LEFT JOIN users ON poems.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        if not results:
            return[]
        poems = []
        for row in results:
            one_poem = cls(row)
            data = {'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                    }
            one_poem.user = user.User(data)
            poems.append(one_poem)
            print(f'**************{poems}')
        return poems

    @classmethod
    def get_all_from_user(cls, user_id):
        query = "SELECT * FROM poems LEFT JOIN users ON poems.user_id = users.id WHERE users.id = %(id)s;"
        data = {'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        all_poems = []
        print(f'**********************{results}')
        for row in results:
            one_poem = cls(row)
            all_poems_creator_info = {
                "id":row['users.id'],
                "first_name":row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
                }
            one_poem.user = user.User(all_poems_creator_info)
            all_poems.append(one_poem)
        return all_poems

    # Update Poems    
    @classmethod
    def update(cls,data):
        query = """UPDATE poems 
                SET title=%(title)s, author=%(author)s, genre=%(genre)s, poem_text=%(poem_text)s
                WHERE id = %(id)s AND poems.user_id = %(user_id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    # Get Poem by ID
    @classmethod
    def get_by_id(cls,data):
        query = """SELECT * FROM poems JOIN users on poems.user_id = users.id 
                WHERE poems.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        if not results:
            return False
        result = results[0]
        poem = cls(result)
        data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password":result['password'],
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        poem.user = user.User(data)
        return poem

    # Validate Poem
    @staticmethod
    def validate_poem(data):
        is_valid = True
        if len(data['title']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False
        if len(data['author']) < 5:
            flash("Author name must be at least 5 characters.")
            is_valid = False
        if len(data['genre']) < 0:
            flash("Genre can not be blank.")
            is_valid = False
        if len(data['poem_text']) < 3:
            flash("Poem text must be at least 3 characters.")
            is_valid = False
        return is_valid

    # Delete Poem
    @classmethod
    def delete(cls,data):
        query = """DELETE FROM poems WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)