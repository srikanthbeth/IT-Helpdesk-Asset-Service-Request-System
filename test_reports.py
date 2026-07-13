def test_reports(test_client):

    response = test_client.get("/reports")

    assert response.status_code in [200, 401, 403]