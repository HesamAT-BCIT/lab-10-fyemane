def test_sensor_data_no_api_key(client):
    response = client.post(
        "/api/sensor_data",
        json={"temperature": 25, "humidity": 50},
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Missing X-API-Key header"


def test_sensor_data_wrong_key(client):
    response = client.post(
        "/api/sensor_data",
        json={"temperature": 25, "humidity": 50},
        headers={"X-API-Key": "wrong-key"},
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


def test_sensor_data_valid_key(client, mock_firestore):
    response = client.post(
        "/api/sensor_data",
        json={"temperature": 25, "humidity": 50},
        headers={"X-API-Key": "test-sensor-key"},
    )

    assert response.status_code == 201
    mock_firestore["collection"].document.assert_called()
    mock_firestore["doc_ref"].set.assert_called_once()