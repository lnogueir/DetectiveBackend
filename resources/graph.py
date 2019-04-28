from flask_restful import Resource, reqparse
from flask import send_file
from models.scrapper import Scrapper
from models.graph import GraphModel
from models.users import UserModel
from threading import Timer
import io

class Graph(Resource):
	parser = reqparse.RequestParser() #Parser so pega o que tem price
	parser.add_argument(
	'url',type=str,
	required=False
	)
	parser.add_argument(
	'filename',type=str,
	required=False
	)
	parser.add_argument(
	'username',type=str,
	required=False
	)
	parser.add_argument(
	'saveAs',type=list,
	required=False
	)



	def get(self):
		param = Graph.parser.parse_args()
		if(param['filename']):
			graph = GraphModel.find_by_filename(param['filename'])
			if graph:
				mimetype='image/png'
				return send_file(io.BytesIO(graph.graph),mimetype=mimetype)
		elif param['username']:
			graphs = GraphModel.find_by_username(param['username'])
			if graphs:
				return [graph.json() for graph in graphs]
		return {'message':'Error, file not found'}, 404
			
		# return send_file(filename['filename'],mimetype='image/png')

	def post(self):
		body = Graph.parser.parse_args()
		username = body['username']
		if UserModel.find_by_username(username):
			scrappy = Scrapper(username,body['url'])
			if len(scrappy.user_map)!=0:
				scrappy.runBS()
				scrappy.makeBarGraph()	
				scrappy.makeExcelFile()
				graph = GraphModel(str(scrappy.scrapper_id),username)
				graph.save_to_db()
				return {'message':'Graphs in production','filename':graph.filename}, 200
			return {'message':'Topic list is empty'}, 400	
		return {'message':'User not found'}	,404


	def put(self):
		body = Graph.parser.parse_args()
		print(body)
		# print(body['saveAs'])
		graphs = GraphModel.find_by_username(body['username'])
		if graphs:
			for i,graph in enumerate(graphs):
				newName = body['saveAs'][i]
				if newName !='' and newName!=None:
					graph.saveAs = body['saveAs'][i]
					graph.save_to_db()
			return {'message':'Graphs saved'}
		return {'message':'User not found'}, 404		

	# def put(self): TO CHANGE JUST ONE
	# 	body = Graph.parser.parse_args()
	# 	graph = GraphModel.find_by_filename(body['filename'])
	# 	if graph:
	# 		graph.saveAs = body['saveAs']
	# 		graph.save_to_db()
	# 		return {'message':'Graph saved as {}'.format(body['saveAs'])}
	# 	return {'message':'File not found'}, 404


	def delete(self):
		filename = Graph.parser.parse_args()
		graph = GraphModel.find_by_filename(filename = filename['filename'])
		if graph:
			graph.delete_from_db()
			return {'message':'Graph deleted'}
		return {'message':'Graph not found'}, 404


		