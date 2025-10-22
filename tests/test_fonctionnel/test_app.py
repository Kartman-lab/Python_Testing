import pytest
import gudlift.server as server

fake_data_competition = [{"name": "competition_test", "date": "2020-03-27 10:00:00", "numberOfPlaces": 10}]
fake_data_club = [{"name": "fake_club", "email": "test@test.co", "points": 10, "booking": 0}]

@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

def test_affichage_welcome_page(client, monkeypatch):
    monkeypatch.setattr(server, "clubs", fake_data_club)
    monkeypatch.setattr(server, "competitions", fake_data_competition)

    response_welcome = client.post('/showSummary', data={"email": "test@test.co"})
    assert response_welcome.status_code == 200

    welcome_page = response_welcome.get_data(as_text=True)

    assert "Welcome, test@test.co" in welcome_page