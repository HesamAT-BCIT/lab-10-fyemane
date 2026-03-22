def auth_header(token="valid-token"):
    return {"Authorization": f"Bearer {token}"}


def test_get_profile_no_auth(client):
    response = client.get("/api/profile")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Missing Authorization header"


def test_get_profile_bad_token_format(client):
    response = client.get(
        "/api/profile",
        headers={"Authorization": "not-bearer-token"},
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid Authorization header format"


def test_get_profile_invalid_token(client, mock_firebase_auth):
    mock_firebase_auth.side_effect = Exception("bad token")

    response = client.get("/api/profile", headers=auth_header("bad-token"))
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid or expired token"


def test_get_profile_success(client, mock_firebase_auth):
    response = client.get("/api/profile", headers=auth_header())

    assert response.status_code == 200
    payload = response.get_json()
    assert "profile" in payload
    assert payload["profile"]["first_name"] == "Test"
    assert payload["profile"]["last_name"] == "User"
    assert payload["profile"]["student_id"] == "12345678"


def test_create_profile_missing_fields(client, mock_firebase_auth):
    response = client.post(
        "/api/profile",
        json={"first_name": "John"},
        headers=auth_header(),
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert "error" in payload or "errors" in payload


def test_create_profile_success(client, mock_firebase_auth, mock_firestore):
    response = client.post(
        "/api/profile",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "student_id": "12345678",
        },
        headers=auth_header(),
    )

    assert response.status_code == 200
    mock_firestore["doc_ref"].set.assert_called_once()


def test_update_profile_invalid_field(client, mock_firebase_auth):
    response = client.put(
        "/api/profile",
        json={"age": 25},
        headers=auth_header(),
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert "error" in payload or "errors" in payload


def test_update_profile_success(client, mock_firebase_auth, mock_firestore):
    response = client.put(
        "/api/profile",
        json={"first_name": "Updated"},
        headers=auth_header(),
    )

    assert response.status_code == 200
    mock_firestore["doc_ref"].set.assert_called_once()


def test_delete_profile_success(client, mock_firebase_auth, mock_firestore):
    response = client.delete("/api/profile", headers=auth_header())

    assert response.status_code == 200
    mock_firestore["doc_ref"].delete.assert_called_once()