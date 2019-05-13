from models.users import UserModel
from collections import defaultdict
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import ssl
from xlwt import Workbook
from db import db 



context = ssl._create_unverified_context()

def getUserMap(username):
	user_map = {}
	user = UserModel.find_by_username(username)
	for topic in user.topics:
		user_map[topic.topic_name] = [tag.json() for tag in topic.tags]
	return user_map

def makeOrderedDict(dic):
    order = OrderedDict()
    l1=[]
    l2=[]
    for key in sorted(dic.items(), key=lambda x:x[1]):
        l1.append(key[0])
        l2.append(key[1])
    l1.reverse()
    l2.reverse()
    i=0
    for item in l1:
        order[item] = l2[i]
        i+=1
    return order


def errorHandling(address):
	try:
		response = urlopen(address,context=context)    
	except HTTPError as e:
		print('Error code: ', e.code)
		return False
	except URLError as e:
		print('Reason: ', e.reason)
		return False
	except ValueError as e:
		print('Error, invalid URL')
		return False
	else:
		return True

def getMaxValDic(dic):
    maximum_val = -1
    for keys in dic:
        if(maximum_val < dic[keys]):
            maximum_val = dic[keys]
            maximum_key = keys
    return maximum_key  

class Scrapper(db.Model):
	__tablename__='scrappers'
	scrapper_id=db.Column(db.Integer,primary_key=True)

	def __init__(self,username,address):
		self.username=username
		self.user_map=getUserMap(username)
		self.topic_points = defaultdict(int)
		self.address = address
		db.session.add(self)
		db.session.commit()



	def runBS(self):
		if errorHandling(self.address):
			page = urllib.request.urlopen(self.address,context=context)
			html = page.read()
			soup = BeautifulSoup(html, 'html.parser')
			content = soup.get_text()
			for script in soup(["script", "style"]):
				script.extract()
			clean_content = content.encode('utf-8')
			validStr = str(clean_content).lower()
			for keys in self.user_map:
				for values in self.user_map[keys]:
					self.topic_points[keys] += validStr.count(values['keyword'].lower())*values['weight']	
		else:
			print('Error reading URL')		

	def makeBarGraph(self):
		order = makeOrderedDict(self.topic_points)
		f=Figure(figsize=(10,10),dpi=100)
		canvas = FigureCanvas(f)
		plotting = f.add_subplot(111)
		# plotting.set_title('Graph build using matplotlib', size=13)
		plotting.set_title('Detective graph for:\n' + str(self.address),size=15)
		plotting.set_xlabel('Topics',fontsize=18)
		plotting.set_ylabel('Points',fontsize=18)
		plt.setp(plotting.get_xticklabels(), rotation='12', fontsize=15)
		howManyIte = 0
		for keys in order:
			if(howManyIte > 6):
				break
			if(howManyIte == 0):
				plotting.bar(keys.capitalize(), order[keys],label='This website is most likely related to ' + str(keys))
			else:
				plotting.bar(keys.capitalize(), order[keys])
			howManyIte+=1
		plotting.legend(loc=1,prop={'size':17})
		# canvas.print_figure('bora kraio')
		filename = str(self.scrapper_id)+'.png'
		f.savefig(filename)
		plt.close()


	def makeExcelFile(self):  
	    wb = Workbook()
	    sheet = wb.add_sheet('Sheet 1',cell_overwrite_ok=True)
	    sheet.write(1,0,'Topics')
	    sheet.write(1,1,'Points')
	    i=2
	    totalPoints=0
	    sheet.write(0,0,'Results for: '+self.address)
	    for elem in self.topic_points:
	       totalPoints+=self.topic_points[elem]
	       sheet.write(i,0,elem)
	       sheet.write(i,1,self.topic_points[elem])
	       i+=1
	    percentage=(self.topic_points[getMaxValDic(self.topic_points)]/totalPoints)*100
	    roundedPercentage = "{0:.2f}".format(round(percentage,2))
	    sheet.write(i,0,'The website '+self.address+' is most likely related to: '+getMaxValDic(self.topic_points))
	    sheet.write(i+1,0,getMaxValDic(self.topic_points)+' corresponds to '+str(roundedPercentage)+'% of the results')
	    filename=str(self.scrapper_id)+'.xls'
	    wb.save(filename)





		

	


