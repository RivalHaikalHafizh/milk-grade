from flask import jsonify, Blueprint,abort
from flask_restful import Resource,Api,reqparse,fields,marshal,marshal_with

import models

message_fields={
    'id':fields.Integer,
    'content':fields.String,
    'published_at':fields.String
}

def get_or_abort(id):
    try:
        msg=models.Message.get_by_id(id)
    except models.Message.DoesNotExist:
        abort(404)
    else:
        return msg


class BaseMessage(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
            required = True,
            help ='konten wajib ada',
            location =['form','args'],

        )
        super().__init__()

class MessageList(BaseMessage):
    def get(self):
        #ambil data dari database
        # messages={}
        # query=models.Message.select()
        messages=[marshal(message,message_fields)for message in models.Message.select()]
        # for row in query:
        #     messages[row.id]={'content':row.content,
        #                         'published_at':row.published_at}
        return {'messages':messages}
        # return jsonify({'messages':messages})

    def post(self):
        args = self.reqparse.parse_args()
        message=models.Message.create(**args)
        # return jsonify({'success':True})
        return marshal(message,message_fields)


class Message(BaseMessage):
    @marshal_with(message_fields)
    def get(self,id):
        # message=models.Message.get_by_id(id)
        return get_or_abort(id)
        # return jsonify({'message':message.content})

    def put(self,id):
        args = self.reqparse.parse_args()
        # msg= get_or_abort(id)
        message=models.Message.update(content=args.get('content')).where(models.Message.id == id).execute()
        return {'messgae':'berhasil mengupdate'}

    def delete(self,id):
        message=models.Message.delete().where(models.Message.id == id).execute()
        return {'messgae':'berhasil menghapus'}
    

messages_api= Blueprint('messages',__name__)
api =Api(messages_api) 

api.add_resource(MessageList, '/messages',endpoint='messages')
api.add_resource(Message, '/message/<int:id>',endpoint='message')