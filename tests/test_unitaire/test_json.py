from unittest.mock import patch, mock_open
import json
from gudlift.server import loadClubs, loadCompetitions, updateJson

fake_data_club = '{"clubs": [{"name": "Test Club", "email": "test@test.com", "points": "10", "booking" : "10"}]}'
fake_data_competiton = '{"competitions": [{"name": "Test Competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": "30"}]}'

def test_loadClubJson():
    with patch("builtins.open", mock_open(read_data=fake_data_club)):
        clubs = loadClubs()
        assert clubs[0]['name'] == "Test Club"
        assert clubs[0]['email'] == "test@test.com"
        assert clubs[0]['points'] == "10"

def test_loadCompetitionJson():
    with patch("builtins.open", mock_open(read_data=fake_data_competiton)):
        competitions = loadCompetitions()
        assert competitions[0]['name'] == "Test Competition"
        assert competitions[0]['date'] == "2020-03-27 10:00:00"

def test_udpateJson():
    data_to_write = [
        {"name": "Test Club 2", "email": "test@test2.com", "points": "20", "booking": "20"}
    ]

    with patch("builtins.open", mock_open(read_data="")) as mocked_file:
        updateJson("fichier_fictif.json", "clubs", data_to_write)
        
        written_content = "".join(call[0][0] for call in mocked_file().write.call_args_list)
        print("Written content:", written_content)

        clubs_file = json.loads(written_content)

        assert "clubs" in clubs_file
        assert clubs_file["clubs"][0]["name"] == "Test Club 2"