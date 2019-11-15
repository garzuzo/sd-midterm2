import pytest
import connexion
import os
from flask import Flask, request, flash, render_template, jsonify,json
from flask_pymongo import pymongo
from bson.json_util import dumps
import importlib.machinery

loader = importlib.machinery.SourceFileLoader('app','backend/app.py')
app = loader.load_module()


flask_app = connexion.FlaskApp(__name__, specification_dir='../openapi/')
flask_app.add_api('my_api.yaml', resolver=connexion.RestyResolver('api'))

#app = connexion.FlaskApp(__name__, specification_dir='openapi/')

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c





def test_valid_read_clients(client):
        
        response = client.get('/users')
        assert response.status_code == 200
    



def test_invalid_endpoint_read_clients(client):
        
        response = client.get('/users/32')
        assert response.status_code == 405
    



def test_valid_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"} 
        response = client.post('/users', data=dict(id='abc12345', name='Marshmillow'), headers=header)
        
        assert response.status_code == 201
        response_remove=client.delete('/users/abc12345')
        assert response_remove.status_code == 204



def test_delete_clients_unavailable(client):
        response_remove=client.delete('/users/juanmaid')
        assert response_remove.status_code == 404


def test_invalid_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"}

        response = client.post('/users', data=dict(id='1', name='Marshmillo'), headers=header)
        
        assert response.status_code == 402
    
def test_invalid_body_req_create_clients(client):
       
        header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"}

        response = client.post('/users', data=dict(id='bcc21912', names='Marshmillo'), headers=header)
        
        assert response.status_code == 400
    
    