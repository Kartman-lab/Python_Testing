import pytest
from gudlift.server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_connexion(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200


def test_connexion_invalid_email(client):
        response = client.post('/showSummary', data={'email': 'notfound@example.com'})
        assert "Email not found." in response.get_data(as_text=True)

def test_competition_or_club_not_found(client):
     response = client.post('/purchasePlaces', data={'competition': 'NomInexistant',
    'club': 'ClubInexistant',
    'places': '1'})
     assert "Competition or club not found." in response.get_data(as_text=True)

def test_place_is_integer(client):
     response = client.post('/purchasePlaces', data={
    'competition': 'Spring Festival',
    'club': 'Simply Lift',
    'places': 'str'})
     assert "Le nombre de places doit être un nombre entier." in response.get_data(as_text=True)


def test_no_more_place_in_competiton(client, monkeypatch):
    fake_competitions = [
        {"name": "Test Competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": 0}
        ]
    fake_clubs = [
            {"name": "Test Club", "email": "test@test.com", "points": "10", "booking": "0"}
            ]
    
    monkeypatch.setattr("gudlift.server.competitions", fake_competitions)
    monkeypatch.setattr("gudlift.server.clubs", fake_clubs)

    response = client.post('/purchasePlaces', data={
         'competition': 'Test Competition',
         'club': 'Test Club',
         'places': '1'
    })

    assert "Il n&#39;y a plus de places disponibles dans cette compétition." in response.get_data(as_text=True)


def test_max_places(client, monkeypatch):
    fake_competitions = [
        {"name": "Test Competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": 20}
        ]
    fake_clubs = [
            {"name": "Test Club", "email": "test@test.com", "points": "10", "booking": "6"}
            ]
    
    monkeypatch.setattr("gudlift.server.competitions", fake_competitions)
    monkeypatch.setattr("gudlift.server.clubs", fake_clubs)

    response = client.post('/purchasePlaces', data={
        'competition': 'Test Competition',
        'club': 'Test Club',
        'places': '7'
    })

    assert "Vous ne pouvez pas réserver plus de 12 places." in response.get_data(as_text=True)

def test_not_enough_place_in_competition(client, monkeypatch):
    fake_competitions = [
        {"name": "Test Competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": 2}
        ]
    fake_clubs = [
            {"name": "Test Club", "email": "test@test.com", "points": "10", "booking": "6"}
            ]
    
    monkeypatch.setattr("gudlift.server.competitions", fake_competitions)
    monkeypatch.setattr("gudlift.server.clubs", fake_clubs)

    response = client.post('/purchasePlaces', data={
        'competition': 'Test Competition',
        'club': 'Test Club',
        'places': '4'
    })

    assert "Il n&#39;y a pas assez de places disponibles dans cette compétition." in response.get_data(as_text=True)

def test_not_enough_points(client, monkeypatch):
    fake_competitions = [
        {"name": "Test Competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": 6}
        ]
    fake_clubs = [
            {"name": "Test Club", "email": "test@test.com", "points": "2", "booking": "6"}
            ]
    
    monkeypatch.setattr("gudlift.server.competitions", fake_competitions)
    monkeypatch.setattr("gudlift.server.clubs", fake_clubs)

    response = client.post('/purchasePlaces', data={
        'competition': 'Test Competition',
        'club': 'Test Club',
        'places': '4'
    })
    assert "Vous n&#39;avez pas assez de points." in response.get_data(as_text=True)
