from models.EmailAccount import Account
import smtplib
from smtplib import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import shutil
from models.graph import GraphModel
import os



def handleArchives(archives): #Make a zip file from the selected items by the user
	if os.path.isdir("tmpdir"):
		shutil.rmtree("tmpdir")
	os.mkdir("tmpdir")  
	for arch in archives:
		graph = GraphModel.find_by_filename(arch['graph']['filename'])
		if graph:
			saveAs = str(arch['graph']['saveAs'])
			if arch['png']:
				with open("tmpdir/"+saveAs+'.png', "wb") as f:
					f.write(graph.graph)
			if arch['xls']:
				with open("tmpdir/"+saveAs+'.xls', "wb") as f:
					f.write(graph.excel)			       
	shutil.make_archive('attachments','zip','tmpdir')  
	return 'attachments.zip'


class EmailSender:
	connected=False
	connection=None
	def __init__(self,username,archives=None,receivers=None):
		self.username=username
		self.emailer=Account()
		self.content=None
		self.archives=archives
		self.receivers=receivers

	def connect(self):
		if not EmailSender.connected:
			try:
				connection = smtplib.SMTP('smtp.gmail.com',587)
				connection.ehlo()
				connection.starttls()
				connection.login(self.emailer.user,self.emailer.password)
			except SMTPResponseException as e:
				error_code=e.smtp_code
				error_message=e.smtp_error
				print('ERROR CONNECTING:'+str(error_message))
			else:
				EmailSender.connected=True
				EmailSender.connection = connection

	@classmethod
	def disconnect(cls):
		if cls.connected:
			cls.connection.close()
			cls.connected=False

	def makeEmail(self):
		if not EmailSender.connected:
			self.connect()
		msg = MIMEMultipart()
		msg["From"]=self.emailer.user
		msg["To"]=",".join(self.receivers)
		msg["Subject"] = "Detective Emailer"
		body = str(len(self.archives)) + " Items from "+self.username
		msg.attach(MIMEText(body,'plain'))
		zip_file=handleArchives(self.archives)
		attachment = open(handleArchives(self.archives),'rb')
		part = MIMEBase('application','octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition',"attachment; filename= "+zip_file)
		msg.attach(part)
		self.content = msg.as_string()
		if os.path.isdir("tmpdir"):
			shutil.rmtree("tmpdir")

	def sendEmail(self):
		if EmailSender.connected:    
			try:
				EmailSender.connection.sendmail(self.emailer.user,self.receivers,self.content)
			except SMTPRecipientsRefused as e:
				refused = e.recipients
				print("ERROR: "+str(e.recipients))
			else:
				print("SUCESS")
				os.remove('attachments.zip')	        






	    
