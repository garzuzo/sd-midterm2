from flask import Flask, request, flash, render_template, jsonify,json
import connexion
from flask_pymongo import pymongo
from bson.json_util import dumps
import os
from flask_cors import CORS, cross_origin
app = connexion.FlaskApp(__name__, specification_dir='../openapi/')
url_mongo="mongodb+srv://"+str(os.environ.get('MONGO_FLASK'))+"@distribuidos-7a22s.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(url_mongo)
db = client.ds_db



#app.run(port=8080)

api_url = '/api'

@app.route(api_url+'/users', methods=['GET'])
@cross_origin(origin='*')
def read_user():
  users=db.Users.find({})
  #print(dumps(list(users)))
  res=dumps(list(users))
  return  res


@app.route(api_url+'/users/<string:id>', methods=['DELETE'])
@cross_origin(origin='*')
def delete_user(id):
  answ=db.Users.delete_one({'id':id}).deleted_count
  if answ==0 :
    resp = jsonify('User does not exist')
    resp.status_code = 404
    return resp
  else :
    resp = jsonify('User removed successfully!')
    resp.status_code = 204
    return resp




@app.route(api_url+'/users', methods=['POST'])
@cross_origin(origin='*')
def create_user():


  id=request.form['id']
  name=request.form['name']
        
  if id and name and request.method == "POST" :
    users=db.Users.find_one({'id':id})
    if users is not None:
      resp = jsonify('User already exists')
      resp.status_code = 402
      return resp
    else:
      db.Users.insert_one({'id': id, 'name':name})
      resp = jsonify('User added successfully!')
      resp.status_code = 201
      return resp
  else :
    resp = jsonify('Bad Request')
    resp.status_code = 400
    return resp

if __name__ == "__main__":
  app.add_api('my_api.yaml', resolver=connexion.RestyResolver('api'))

  app.run(port=3000, debug=True)
    
