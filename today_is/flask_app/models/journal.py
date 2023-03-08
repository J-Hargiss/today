from sqlite3 import connect
from flask_app.__init__ import app
from flask_app.config.mysqlconnect import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re
bcrypt = Bcrypt(app)


class Journal:
    db = "today_is"
    
    def __init__(self, data):
        self.id = data["id"]
        self.what_happend = data["what_happend"]
        self.new_symptom = data["new_symptom"]
        self.tool_used = data["tool_used"]
        self.effective = data["effective"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data['user_id']
        self.user = None


    @classmethod
    def get_all_journals(cls):
        query = "SELECT * FROM journals;"
        results = connectToMySQL('today_is').query_db(query)
        journal_objects = []
        for row in results:
            journal_objects.append(cls(row))
        print(results)
        return journal_objects 
    
    @classmethod
    def get_by_id(cls, result_id):
        data = {"id": result_id}
        query = "SELECT * FROM journals JOIN users on users.id = journals.user_id WHERE journals.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def save_journal(cls,data):
        query = '''INSERT INTO journals (what_happend, new_symptom, tool_used, effective, user_id) 
            VALUES (%(what_happend)s,%(new_symptom)s,%(tool_used)s,%(effective)s,%(user_id)s);'''
        results = connectToMySQL("today_is").query_db(query,data)
        print(results)
        return results
    
    @staticmethod
    def validate_new_journal(data):
        is_valid = True

        if len(data['what_happend']) <3:
            flash('Cannot leave what happened blank','journal')
            is_valid = False

        if len(data['new_symptom'])< 3:
            flash('Cannot leave symptoms blank', 'journal')
            is_valid = False
        
        if len(data['tool_used']) < 1:
            flash('Please select a tool','journal')
            is_valid = False
        
        if 'effective' not in data: 
            flash('Please specify if tool was effective','journal')
            is_valid = False
        
        return is_valid

    @classmethod
    def update_journal(cls, entry):
        query = '''UPDATE journals SET what_happend = %(what_happend)s, new_symptom = %(new_symptom)s, tool_used = %(tool_used)s,
                effective = %(effective)s WHERE id = %(id)s;'''
        results = connectToMySQL("today_is").query_db(query, entry)
        entry = cls.get_by_id(entry['id'])
        return results




    @classmethod
    def delete_journal(cls, journal_id):
        data = {"id": journal_id}
        query = 'DELETE FROM journals WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def journalUser(cls,data):
        query = '''SELECT * FROM journals LEFT JOIN users 
                ON journals.user_id = users.id WHERE journals.id = %(id)s;'''
        results = connectToMySQL(cls.db).query_db(query,data)
        print("journalUser results", results)
        allJournals = []
        for row in results:
            book = cls(results[0])
            userData = {
                'id': row['users.id'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            print('userdata', userData)
            oneUser = user.User(userData)
            book.user = oneUser
            allJournals.append(book)
            print('allJournals', allJournals)
        return allJournals
    
