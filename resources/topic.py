from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.topic import TopicModel


class Topic(Resource):
    def get(self,username,topic_name):
        topic = TopicModel.find_by_topic(username,topic_name)
        if topic:
            return topic.json()
        return {'message':'Topic not found'},404


    def post(self,username,topic_name):
        topic = TopicModel.find_by_topic(username,topic_name)
        if topic:
            return {'message':"Error, topic with name '{}' already exists".format(topic_name)}, 400
        topic = TopicModel(username,topic_name)
        try:
            topic.save_to_db()
        except:
            return {'message':"Error saving store"}, 500
        return topic.json(), 201

    def delete(self,username,topic_name):
        delTopic = TopicModel.find_by_topic(username,topic_name)
        if delTopic:
            delTopic.delete_from_db()
            return {'message':'Item deleted'}
        return {'message':'Item not found'}, 404    

class TopicList(Resource):
    def get(self,topic_name):
        return {'topics':[topic.json() for topic in TopicModel.find_all_topic(topic_name)]}
