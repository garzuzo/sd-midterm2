import pytest
import connexion




@pytest.fixture(scope='module')
def client():
    flask_app = connexion.FlaskApp(__name__)
    with flask_app.app.test_client() as c:
        yield c


def test_get_health(client):
    # GIVEN ...
    # WHEN I access to the url ...
    # THEN ...
    response = client.get('/health')
    assert response.status_code == 200
