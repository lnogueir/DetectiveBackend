from EmailAccount import Account
import smtplib
from smtplib import *
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import shutil



def handleArchives(archives):
	os.mkdir('tmpdir')  
    for arch in archives:
    	if arch.png:
   			with open("tmpdir/"+str(arch.saveAs)+'.png', "wb") as f:
				f.write(arch.graph)
		if arch.xls:
			with open("tmpdir/"+str(arch.saveAs)+'.xls', "wb") as f:
				f.write(arch.excel)			       
    shutil.make_archive('attachments','zip','tmpdir')  
    return 'attachments.zip'


class EmailSender:
	def __init__(self,username,archives=None,receivers=None):
		self.username=username
		self.emailer=Account()
		self.connected=False
		self.connection=None
		self.content=None
		self.archives=archives
		self.receivers=receivers

	def connect(self):
		try:
			connection = smtplib.SMTP('smtp.gmail.com',587)
			connection.ehlo()
			connection.starttls()
			connection.login(self.emailer.user,self.emailer.password)
		except SMTPResponseException as e:
			error_code=e.smtp_code
			error_message=e.smtp_error
			print('ERROR CONNECTING:'+str(error_code,error,error_message))
		else:
			self.connected=True
			self.mail = mail

	def disconnect(self):
		if self.connected:
			self.mail.close()

	def makeEmail(self):
		if not self.connected:
			self.connect()
		msg = MIMEMultipart()
	    msg["From"]=self.emailer.user
	    msg["To"]=",".join(receivers)
	    msg["Subject"] = "Detective Emailer"
	    body = str(len(archives)) + " Items from "+self.username
	    msg.attach(MIMEText(body,'plain'))
	    zip_file=handleArchives(self.archives)
	    attachment = open(handleArchives(self.archives),'rb')
	    part = MIMEBase('application','octet-stream')
	    part.set_payload((attachment).read())
	    encoders.encode_base64(part)
	    part.add_header('Content-Disposition',"attachment; filename= "+zip_file)
	    msg.attach(part)
	    self.content = msg.as_string()
	    os.rmdir('tmpdir/')

	def sendEmail(self,receivers):
		if self.connected:    
			try:
		    	mail.sendmail(self.username,receivers,self.content)
		    except SMTPRecipientsRefused as e:
		    	refused = e.recipients
		    	print("ERROR: "+str(e.recipients))
		    else:
		        print("SUCESS")
		        os.remove('attachments.zip')	        






	    
