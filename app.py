import pandas as pd
import sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import gevent.pywsgi
import joblib
from flask_jwt_extended import (JWTManager,jwt_required,
                                create_access_token,get_jwt_identity)


import models
from resources.messages import messages_api
from resources.users import users_api
from resources.milks import milks_api



app = Flask(__name__,static_url_path='/static')
CORS(app, support_credentials=True)
#ACCESS_TOKEN_JWT
app.config['SECRET_KEY'] ='scfsdsdfsdfsferwer'
app.config['JWT_BLACKLIST_ENABLED'] =True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] =['access,refresh']
jwt=JWTManager(app)

app.register_blueprint(messages_api,url_prefix='/api/v1')
app.register_blueprint(users_api,url_prefix='/api/v1')
app.register_blueprint(milks_api,url_prefix='/api/v1')

@app.route('/api/v1/clasifier',methods=["POST"])
def classifier():
    pipe = joblib.load('model.pkl')
    # New data to predict
    d = {
        'Temprature': -0.877314,
        'Odor': 1.2741591,
        'Fat ': 0.729325,
        'Turbidity': 1.434086,
        'merge': 0.063744
    }
    pr = pd.DataFrame(d, index=[0])
    pred_cols = list(pr.columns.values)[:]
    # apply the whole pipeline to data
    pred = pd.Series(pipe.predict(pr[pred_cols]))
    print(pr)
    return jsonify(pred[0])

#logout
blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti=decrypted_token['jti']
    return jti in blacklist

@app.route('/api/v1/user/logout')
def logout():
    return {'msg':'berhasil logout'}
# api = Api(app)

# users = {}

# class User(Resource):
#     def get(self,user_id):
#         return {'nama':users[user_id]}

#     def put(self, user_id):
#         users[user_id] = request.form['user']
#         return {'nama': users[user_id]}

# api.add_resource(messages.MessageList, '/messages')


if __name__ == '__main__':
    models.initialize()   
    # Untuk mode pengembangan
    app.run(debug=True)

    # Gunakan wsgi server untuk deployment (production)
    # http_server = gevent.pywsgi.WSGIServer(("127.0.0.1", 80), app)
    # http_server.serve_forever()
