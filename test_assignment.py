def get_token(test_client):

    response = test_client.post(
        "/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "admin123"
        }
    )

    return response.json()["access_token"]


def test_support_requests(test_client):

    token = get_token(test_client)

    response = test_client.get(
        "/support/1/requests",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 404]