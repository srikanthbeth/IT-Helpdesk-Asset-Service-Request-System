def test_register(test_client):

    response = test_client.post(
        "/auth/register",
        json={
            "name":"Admin",
            "email":"admin@gmail.com",
            "password":"admin123",
            "role":"Admin"
        }
    )

    if response.status_code == 400:
        assert response.json()["detail"] == "Email already registered"
    else:
        assert response.status_code in [200, 201]