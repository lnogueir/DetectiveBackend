from db import db
class TopicModel(db.Model):
    __tablename__='topics'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),db.ForeignKey('users.username'))
    topic_name=db.Column(db.String(80))
    tags = db.relationship('TagModel')

    def __init__(self,username,topic_name):
        self.username = username
        self.topic_name=topic_name

    def json(self):
        return {'id':self.id,'topic':self.topic_name,'tags':[tag.json() for tag in self.tags]}

    @classmethod
    def find_by_topic(cls,username,topic_name):
        return cls.query.filter_by(username=username).filter_by(topic_name=topic_name).first() #SELECT * FROM __tablename__ WHERE name=name LIMIT 1

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id)    

    @classmethod
    def find_all_topic(cls,topic_name):
        return cls.query.filter_by(topic_name=topic_name)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
