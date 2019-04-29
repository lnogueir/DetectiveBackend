from flask_restful import Resource, reqparse
from models.friends import FriendModel
from models.users import UserModel

class Friend(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
	'contact_name',type=str,
	required=True
	)

	def get(self,username):
		friends = FriendModel.find_by_username(username)
		if friends:
			you = [{"contact_name":UserModel.find_by_username(username).email}]
			return {'friends':you+[friend.json() for friend in friends]}
		else:
			return {'message':'User not found'}, 404

	def post(self,username):
		body = Friend.parser.parse_args()
		if FriendModel.find_by_contact(username,body['contact_name']):
			return {'message':"A friend with contact '{}' already exists.".format(body['contact_name'])}, 400
		friend = FriendModel(username,body['contact_name'])
		try:
			friend.save_to_db()
		except:
			return {'message':'Exception raised when inserting item'},500
		return friend.json(), 201 #201 is CREATED


	def put(self,username):
		body = Friend.parser.parse_args()
		friends = FriendModel.find_by_username(username)
		newNames = body['contact_name'].split(',')
		print(newNames)
		if friends:
			for i,friend in enumerate(friends):
				newName = newNames[i]
				# print(newName)
				if newName !='' and newName!=None:
					friend.contact_name = newName
					friend.save_to_db()
					print(newName)
			return {'message':'Contacts edited'}
		return {'message':'User not found'}, 404


	def delete(self,username):
		body = Friend.parser.parse_args()
		friend = FriendModel.find_by_contact(username,body['contact_name'])
		if friend:
			friend.delete_from_db()
			return {'message':'Friend removed'}
		else:
			return {'message':'Friend not found'}, 404




