from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
from resources.users import UserRegister,User
from resources.tags import Tag,Tags
from resources.topic import Topic,TopicList
from resources.graph import Graph
from resources.emailer import Email
from resources.friends import Friend
from ip import ip

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123456'

api = Api(app)
@app.before_first_request
def create_tables():
    db.create_all()



jwt = JWT(app,authentication,identity)


api.add_resource(UserRegister,'/register')
api.add_resource(User,'/user/<string:username>')
api.add_resource(Topic,'/topic/<string:username>/<string:topic_name>')
api.add_resource(TopicList,'/topics/<string:topic_name>')
api.add_resource(Tag,'/tag/<int:topic_id>/<string:keyword>')
api.add_resource(Tags,'/tags/<int:topic_id>')
api.add_resource(Graph,'/graph')
api.add_resource(Email,'/email/<string:username>')
api.add_resource(Friend,'/friend/<string:username>')




if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000,host=ip())
