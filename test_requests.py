def test_get_requests(test_client):

    response = test_client.get("/requests")

    assert response.status_code in [200, 401, 403]