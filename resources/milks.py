from flask import jsonify, Blueprint, abort,make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
import json
from joblib import dump, load  # For serialization. Pre-installed by sklearn.
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib
import models
from flask_jwt_extended import (JWTManager, jwt_required,
                                create_access_token, get_jwt_identity)

milk_fields = {
    'Temprature': fields.Integer,
    'Odor': fields.Integer,
    'Fat ': fields.Integer,
    'Turbidity': fields.Integer,
    'Grade': fields.String
}


class MilkBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'Temprature',
            required=True,
            help='Temprature wajib ada',
            location=['form', 'args'],

        )
        self.reqparse.add_argument(
            'Odor',
            required=True,
            help='Odor wajib ada',
            location=['form', 'args'],

        )
        self.reqparse.add_argument(
            'Fat ',
            required=True,
            help='Fat wajib ada',
            location=['form', 'args'],

        )
        self.reqparse.add_argument(
            'Turbidity',
            required=True,
            help='Turbidity wajib ada',
            location=['form', 'args'],

        )
        super().__init__()


class Milk(MilkBase):
    def post(self):
        args = self.reqparse.parse_args()
        Temprature = args.get('Temprature')
        Odor = args.get('Odor')
        Fat  = args.get('Fat ')
        Turbidity = args.get('Turbidity')
        pipe = joblib.load('../milk-grade/my_model.pkl')
        d = {
                'Temprature': int(Temprature),
                'Odor': int(Odor),
                'Fat ': int(Fat),
                'Turbidity': int(Turbidity),
            }
        pr = pd.DataFrame(d, index=[0])
        same_standard_scaler = load('../milk-grade/my-standard-scaler.pkl') 
        pr[:] = same_standard_scaler.transform(pr.loc[:])
        pred_cols = list(pr.columns.values)[:]
        # # apply the whole pipeline to data
        pred = pd.Series(pipe.predict(pr[pred_cols]))
        Grade =pred[0]
        milks = models.MilkGrade.create(
            Temprature=Temprature,
            Odor=Odor,
            Fat=Fat,
            Turbidity=Turbidity,
            Grade=Grade
        )
        return jsonify({'feature anda':d,'Grade hasil prediksi':Grade})




milks_api = Blueprint('milks', __name__)
api = Api(milks_api)

api.add_resource(Milk, '/clasifier', endpoint='clasifier')
