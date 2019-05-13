from db import db

class FriendModel(db.Model):
	__tablename__='friends'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(80),db.ForeignKey('users.username'))
	contact_name=db.Column(db.String(80))
	
	def __init__(self,username,contact_name):
		self.username=username
		self.contact_name=contact_name

	def json(self):
		return {'contact_name':self.contact_name}

	@classmethod
	def find_by_username(cls,username):
		return cls.query.filter_by(username=username)

	@classmethod
	def find_by_contact(cls,username,contact_name):
		return cls.query.filter_by(username=username).filter_by(contact_name=contact_name).first() #SELECT * FROM __tablename__ WHERE name=name LIMIT 1
		

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()





