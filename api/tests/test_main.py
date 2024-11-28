import pytest

def test_api_endpoint():
    response = client.get('/api/endpoint')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_api_response_format():
    response = client.get('/api/endpoint')
    assert isinstance(response.json(), dict)