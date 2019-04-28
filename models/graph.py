from db import db
import os

def processedFile(filename):
	print(filename)
	with open(filename, "rb") as f:
		return f.read()


class GraphModel(db.Model):
	__tablename__='graphs'
	id=db.Column(db.Integer,primary_key=True)
	filename=db.Column(db.String(80))
	username=db.Column(db.String(80),db.ForeignKey('users.username'))
	saveAs=db.Column(db.String(30))
	graph=db.Column(db.LargeBinary)
	excel=db.Column(db.LargeBinary)	

	def __init__(self,filename,username):
		print(filename)
		self.filename=filename
		self.username=username
		self.saveAs=None 
		self.graph=processedFile(filename+'.png')
		self.excel=processedFile(filename+'.xls')
		os.remove(filename+'.png')
		os.remove(filename+'.xls')
		

	def json(self):
		return {'filename':self.filename,'saveAs':self.saveAs}

	@classmethod
	def find_by_filename(cls,filename):
		return cls.query.filter_by(filename=filename).first()

	@classmethod
	def find_by_username(cls,username):
		return cls.query.filter_by(username=username)	

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
