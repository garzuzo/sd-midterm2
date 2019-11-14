import pytest
import connexion
import os
from flask import Flask, request, flash, render_template, jsonify,json
from flask_pymongo import pymongo
import app


flask_app = connexion.FlaskApp(__name__, specification_dir='../openapi/')
flask_app.add_api('my_api.yaml', resolver=connexion.RestyResolver('api'))

#app = connexion.FlaskApp(__name__, specification_dir='openapi/')

@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c



def test_read_clients(client):
        
        response = client.get('/users')
        assert response.status_code == 200
    
def test_cread_clients(client):
        
        response = client.get('/users')
        assert response.status_code == 200
    
    
    
    