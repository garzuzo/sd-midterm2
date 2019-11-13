import pytest
import connexion
import os
from flask import Flask, request, flash, render_template, jsonify,json
from flask_pymongo import pymongo
#app = connexion.FlaskApp(__name__, specification_dir='openapi/')



@pytest.fixture(scope='module')
def init_db():
        url_mongo=os.environ['MONGO_FLASK']
        client = pymongo.MongoClient(url_mongo)
        db = client.ds_db
        yield db 
        
@pytest.fixture(scope='module')
def client():
        flask_app=Flask(__name__)
        testing_client = flask_app.test_client()
        # Establish an application context before running the tests.
        ctx = flask_app.app_context()
        ctx.push()
 
        yield testing_client  # this is where the testing happens!
 
        ctx.pop()


def test_get_clients(client):
    response = client.get('/api/users')
    assert response.status_code == 200