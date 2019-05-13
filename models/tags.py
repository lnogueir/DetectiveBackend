from db import db
from models.topic import TopicModel



def fixWeight(topic_id,keyword,isAdding):
    query_result = TopicModel.find_by_id(topic_id).first()
    if query_result:
        topic_name = query_result.json()['topic']
        topics = TopicModel.find_all_topic(topic_name)
        weight = (1 if isAdding else 0)
        for topic in topics:
            print(topic.json())
            for tag in topic.tags:
                if tag.keyword==keyword:
                    weight+=1
                    break

        for topic in topics:
            for tag in topic.tags:
                if tag.keyword==keyword:
                    tag.weight = weight 
                    break
            topic.save_to_db()     
        return weight
    else:
        return None                    



class TagModel(db.Model):
    __tablename__='tags'
    id=db.Column(db.Integer,primary_key=True)
    topic_id=db.Column(db.Integer,db.ForeignKey('topics.id'))
    keyword=db.Column(db.String(80))
    weight=db.Column(db.Integer)
    # store = db.relationship('StoreModel')

    def __init__(self,keyword,topic_id):
        self.keyword=keyword
        self.weight=fixWeight(topic_id,keyword,True)
        self.topic_id = topic_id

    def json(self):
        return {'keyword':self.keyword,'weight':self.weight}

    @classmethod
    def find_by_name(cls,topic_id,keyword):
        return cls.query.filter_by(topic_id=topic_id).filter_by(keyword=keyword).first() #SELECT * FROM __tablename__ WHERE name=name LIMIT 1


    @classmethod
    def find_tags_by_id(cls,topic_id):
        return cls.query.filter_by(topic_id=topic_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
