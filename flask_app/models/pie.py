from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

mydb = 'beltexam'

class Pie:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.votes = data['votes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.creator = None
        

    @staticmethod
    def validate_pie(pie_data):
        is_valid = True
        #print(order_data['type'])
        if len(pie_data['name']) < 1:
            is_valid = False
            flash('Name Required')
        if len(pie_data['filling']) < 1:
            is_valid = False
            flash('Filling Required')
        if len(pie_data['crust']) < 1:
            is_valid = False
            flash('Crust Required')
        return is_valid

    @classmethod
    def save(cls, data):
        query = '''
        INSERT INTO pies
        (name, filling, crust, creator_id)
        VALUES (%(name)s, %(filling)s, %(crust)s, %(creator_id)s);
        '''
        results = connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def get_by_user_id(cls, data):
        query = '''
        SELECT *
        FROM pies
        WHERE creator_id = %(id)s;
        '''
        results = connectToMySQL(mydb).query_db(query, data)
        output = []
        for pie in results:
            this_pie = cls(pie)
            output.append(this_pie)
        return output

    @classmethod
    def get_by_id(cls, data):
        query = '''
        SELECT * 
        FROM pies
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)
        return cls(results[0])

    @classmethod
    def delete_by_id(cls, data):
        query = '''
        DELETE FROM pies
        WHERE id = %(id)s
        '''

        connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def update_pie(cls, data):
        query = '''
        UPDATE pies
        SET name = %(name)s, filling = %(filling)s, crust = %(crust)s
        WHERE id = %(id)s;
        '''

        results = connectToMySQL(mydb).query_db(query, data)
        print(results)

    @classmethod
    def get_all_join_creator_by_id(cls, data):
        query = '''
        Select * 
        FROM pies
        JOIN users
        ON
        pies.creator_id = users.id
        WHERE pies.id = %(id)s;
        '''
        
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)
        for pie in results:
            this_pie = cls(pie)
            user_data = {
                'id': pie['users.id'],
                'first_name': pie['first_name'],
                'last_name': pie['last_name'],
                'email': pie['email'],
                'password': pie['password'],
                'created_at': pie['users.created_at'],
                'updated_at': pie['users.updated_at']
            }
            this_pie.creator = user.User(user_data)
        return this_pie


    @classmethod
    def get_all_join_creator(cls):
        query = '''
        Select * 
        FROM pies
        JOIN users
        ON
        pies.creator_id = users.id;
        '''
        results = connectToMySQL(mydb).query_db(query)
        print(results)
        output = []
        for pie in results:
            this_pie = cls(pie)
            user_data = {
                'id': pie['users.id'],
                'first_name': pie['first_name'],
                'last_name': pie['last_name'],
                'email': pie['email'],
                'password': pie['password'],
                'created_at': pie['users.created_at'],
                'updated_at': pie['users.updated_at']
            }
            this_pie.creator = user.User(user_data)
            output.append(this_pie)
        return output

    @classmethod
    def add_vote(cls, data):
        query = '''
        UPDATE pies
        SET votes = votes +1
        WHERE id = %(id)s;
        '''

        connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def delete_vote(cls, data):
        query = '''
        UPDATE pies
        SET votes = votes -1
        WHERE id = %(id)s;
        '''

        connectToMySQL(mydb).query_db(query, data)