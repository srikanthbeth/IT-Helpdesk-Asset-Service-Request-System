def test_get_assets(test_client):

    response = test_client.get("/assets")

    assert response.status_code in [200, 401, 403]