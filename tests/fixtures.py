import pytest


test_dict = {
    "name": "Face Lift",
    "email": "johnsteed@hotmail.com",
    "points": "50",
    "competition": "Spring Festival",
    "date": "2022-03-27 10:00:00",
    "numberOfPlaces": "25",
    "bookedPlaces": "2"
}


def mock_load_clubs():
    """
    A function that returns a mock list of clubs.
    """
    list_of_clubs = [
        {
            "name": "Face Lift",
            "email": "johnsteed@hotmail.com",
            "points": "50"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]
    return list_of_clubs


@pytest.fixture
def fixture_load_clubs(monkeypatch):
    """
    A fixture to replace actual list of clubs with a mock list of clubs.
    """
    monkeypatch.setattr('server.clubs', mock_load_clubs())


def mock_load_competitions():
    """
    A function that returns a mock list of competitions.
    """
    list_of_competitions = [
        {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
    return list_of_competitions


@pytest.fixture
def fixture_load_competitions(monkeypatch):
    """
    A fixture to replace actual list of competitions with a mock list of
    competitions.
    """
    monkeypatch.setattr('server.competitions', mock_load_competitions())
