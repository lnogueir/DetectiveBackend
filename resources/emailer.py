from models.emailer import EmailSender
from models.graph import GraphModel
from flask_restful import Resource, reqparse



class Email(Resource):
	parser = reqparse.RequestParser() #Parser so pega o que tem price
	parser.add_argument(
	'archives',type=list,
	required=True
	)
	parser.add_argument(
	'receivers',type=list,
	required=True
	)
	
	def post(self,username):
		body = Email.parser.parse_args()
		# print(body)
		emailer = EmailSender(username,body['archives'],body['receivers'])
		emailer.connect()
		emailer.makeEmail()
		emailer.sendEmail()
		emailer.disconnect()
		return {'message':'Email has been successfully sent to {}'.format(emailer.receivers)}