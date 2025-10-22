import pytest
import json 
import gudlift.server as server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

fake_data_competition = [{"name": "competition_test", "date": "2020-03-27 10:00:00", "numberOfPlaces": 10}]
fake_data_club = [{"name": "fake_club", "email": "test@test.co", "points": 10, "booking": 0}]

def test_booking(client, monkeypatch):
    monkeypatch.setattr(server, "clubs", fake_data_club)
    monkeypatch.setattr(server, "competitions", fake_data_competition)
 
    response_welcome = client.post('/showSummary', data={'email': 'test@test.co'})
    assert response_welcome.status_code == 200 

    response_purchase_places = client.post('/purchasePlaces', data={'competition': 'competition_test',
                                        'club': 'fake_club',
                                        'places': '4'})
    
    
    assert 'Réservation de 4 places pour fake_club dans la compétition competition_test réussie!'
    'Il reste 6 places dans competition_test. '
    'Points restants pour fake_club : 6' in response_purchase_places.get_data(as_text=True)
    
    assert fake_data_competition[0]["numberOfPlaces"] == 6
    assert fake_data_club[0]["points"] == 6

    response_purchase_places_again = client.post('/purchasePlaces', data={'competition': 'competition_test',
                                                                          'club': 'fake_club',
                                                                          'places': '7'})
    
    assert "Il n&#39;y a pas assez de places disponibles dans cette compétition." in response_purchase_places_again.get_data(as_text=True)
