from flask import Flask, request, flash, render_template, jsonify,json
import connexion
from flask_pymongo import pymongo
from bson.json_util import dumps
import os

app = connexion.FlaskApp(__name__, specification_dir='openapi/')
#app=Flask(__name__)
#app.config['DEBUG'] = True
url_mongo=os.environ['MONGO_FLASK']
client = pymongo.MongoClient(url_mongo)
db = client.ds_db



#app.run(port=8080)

api_url = '/api'

@app.route(api_url+'/users', methods=['GET'])
def read_user():
  users=db.Users.find({})
  #print(dumps(list(users)))
  res=dumps(list(users))
  return  res


@app.route(api_url+'/users', methods=['POST'])
def create_user():
  id=request.form['id']
  name=request.form['name']
        
  if id and name and request.method == "POST" :
    id = db.Users.insert({'id': id, 'name':name})
    resp = jsonify('User added successfully!')
    resp.status_code = 200

    return resp


  else :
    return not_found()

if __name__ == "__main__":
  app.add_api('my_api.yaml', resolver=connexion.RestyResolver('api'))
  app.run()
    
