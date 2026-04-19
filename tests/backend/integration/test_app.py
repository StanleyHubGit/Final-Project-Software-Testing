def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json


def test_global_error_handler(client):
    @client.application.route("/error")
    def trigger_error():
        raise Exception("test error")

    response = client.get("/error")
    assert response.status_code == 500
    assert "error" in response.json