from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.tags import TagModel,fixWeight


class Tag(Resource):
    #BOTA NA CLASSE PARA NAO FICAR COPIANDO E COLANDO
    # parser = reqparse.RequestParser() #Parser so pega o que tem price
    # parser.add_argument(
    #     'weight',type=float,
    #     required=True,help='This field cannot be blank'
    # )

    # parser.add_argument(
    #     'topic_id',type=int,
    #     required=True,help='Every item needs a store id'
    # )

    # @jwt_required()
    def get(self,topic_id,keyword):
        tag = TagModel.find_by_name(topic_id,keyword)
        if tag:
            return tag.json()
        return {'message':'Tag not found'}, 404

    def post(self,topic_id,keyword):
        if TagModel.find_by_name(topic_id,keyword):
            return {'message':"A tag with name '{}' already exists.".format(keyword)}, 400
        # data = Tag.parser.parse_args() #This makes sure we only get the price, even if there are more stuff in the body
        item = TagModel(keyword,topic_id)
        try:
            item.save_to_db()
        except:
            return {'message':'Exception raised when inserting item'},500
        return item.json(), 201 #201 is CREATED

    def delete(self,topic_id,keyword):
        tag = TagModel.find_by_name(topic_id,keyword)
        if tag:
            tag.delete_from_db()
            fixWeight(topic_id,keyword,False)
            return {'message':'Item deleted'}
        return {'message':'Item not found'}, 404


    # def put(self,topic_id,keyword):
    #     data = Tag.parser.parse_args() #request.get_json() Isso pega tudo que o cara manda no body
    #     tag = TagModel.find_by_name(topic_id,keyword)
    #     if tag is None:
    #         tag = TagModel(keyword,data['weight'],topic_id)
    #     else:
    #         tag.weight=data['weight']
    #     item.save_to_db()
    #     return item.json()

class Tags(Resource):
    def get(self,topic_id):
        tags = TagModel.find_tags_by_id(topic_id)
        if tags:
            return {'tags':[tag.json() for tag in tags]}
        return {'message':'Topic id not found'}, 404    

    def delete(self,topic_id):
        tags = TagModel.find_tags_by_id(topic_id)

        if tags:
            # print('chamou a funcao')
            for tag in tags:
                tag.delete_from_db()
                fixWeight(topic_id,tag.keyword,False)
            return {'message':'Tags for topic id {} have been deleted'.format(topic_id)}            
        return {'message':'Topic id not found'}, 404



class TagList(Resource):
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}
