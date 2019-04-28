import sqlite3
from flask_restful import Resource, reqparse
from models.users import UserModel
from security import hash_password



class User(Resource):
    # @jwt_required()
    def get(self,username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        return {'message':'User not found'}, 404



class UserRegister(Resource):
    parser = reqparse.RequestParser() #Parser so pega o que tem price
    parser.add_argument(
        'username',type=str,
        required=True,help='You must enter a username'
    )
    parser.add_argument(
        'password',type=str,
        required=True,help='You must enter a password'
    )
    parser.add_argument(
        'email',type=str,
        required=True,help='You must enter an email'
    )


    def post(self):
        newUser = UserRegister.parser.parse_args()
        if UserModel.find_by_username(newUser['username']):
            return {'message':'Username already exists'}, 400
        user = UserModel(newUser['username'],hash_password(newUser['password']),newUser['email'])
        user.save_to_db()
        return {'message':'User created successfully'}
