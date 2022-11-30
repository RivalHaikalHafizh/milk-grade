from flask import jsonify, Blueprint, abort,make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
from hashlib import md5
import json
import models
from flask_jwt_extended import (JWTManager, jwt_required,
                                create_access_token, get_jwt_identity)

user_fields = {
    'username': fields.String,
    'access_token': fields.String
}


class UserBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='username wajib ada',
            location=['form', 'args'],

        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='password wajib ada',
            location=['form', 'args'],

        )
        super().__init__()


class UserList(UserBase):
    def post(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            models.User.select().where(models.User.username == username).get()
        except models.User.DoesNotExist:
            # daftarun usernya
            user = models.User.create(
                username=username,
                password=md5(password.encode('utf-8')).hexdigest()
            )
            access_token = create_access_token(identity=username)
            user.access_token = access_token
            return marshal(user, user_fields)
        else:
            raise Exception('username sudah terdaftar')

    @jwt_required(optional=False)
    def get(self):
        return {'message': 'data yangterproteksi'}


class User(UserBase):
    def post(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            hashpassword = md5(password.encode('utf-8')).hexdigest()
            username = models.User.get((models.User.username == username) & (
                models.User.password == hashpassword))
        except models.User.DoesNotExist:
            # daftarun usernya
            return {'message': 'user or passsword is wrong'}
        else:
            username = args.get('username')
            access_token = create_access_token(identity=username)
            return {'message': 'selamat login','token':access_token}


users_api = Blueprint('users', __name__)
api = Api(users_api)

api.add_resource(UserList, '/user/register', endpoint='user/registr')
api.add_resource(User, '/user/signin', endpoint='user/signin')
