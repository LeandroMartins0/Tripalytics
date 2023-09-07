from app import app

def test_home_endpoint():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Jobsity Technical Test!" in response.data
