import json
import pytest
import server

TEST_DICT = {
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
    Fonction qui récupère la liste des clubs du fichier test_clubs.json.

    Retourne une liste de dictionnaires
    """
    with open('tests/tests_integration/test_clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


@pytest.fixture
def fixture_load_clubs(monkeypatch):
    """
    Une fixture permettant de remplacer la liste actuelle des clubs par une liste factice de clubs.
    """
    monkeypatch.setattr('server.clubs', mock_load_clubs())


def mock_load_competitions():
    """
    Fonction qui récupère la liste des compétitions à partir du fichier test_competitions.json.

    Retourne une liste de dictionnaires
    """
    with open('tests/tests_integration/test_competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


@pytest.fixture
def fixture_load_competitions(monkeypatch):
    """
    Une fixture pour remplacer la liste réelle des concours par une liste fictive de concours.
    """
    monkeypatch.setattr('server.competitions', mock_load_competitions())


class TestIntegration:
    """
    Une classe qui regroupe les tests des fonctions suivantes :
    loadClubs
    loadCompetitions
    index
    showSummary
    book
    purchasePlaces
    displayClubsPoints
    logout
    """

    def test_load_clubs(self):
        """
        Une fonction qui teste le chargement du fichier json des clubs.
        """
        assert len(mock_load_clubs()) == 3
        assert mock_load_clubs()[0] == {
            "name": "Face Lift",
            "email": "johnsteed@hotmail.com",
            "points": "50"
        }

    def test_load_competitions(self):
        """
        Une fonction qui teste le chargement du fichier json des compétitions.
        """
        assert len(mock_load_competitions()) == 2
        assert mock_load_competitions()[0] == {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        }

    def test_index(self):
        """
        Teste si la vue de l'index fonctionne en vérifiant le code d'état de la réponse.
        """
        response = server.app.test_client()
        assert response.get('/').status_code == 200

    def test_show_summary(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste l'accès à la vue showSummary avec une adresse électronique valide enregistrée.
        """
        email = TEST_DICT.get("email", "alternate@hotmail.com")
        response = server.app.test_client().post('/showSummary',
                                                 data=dict(email=email))
        assert response.status_code == 200
        assert f"Welcome, {email}".encode("utf-8") in response.data

    def test_book(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste si la vue book fonctionne en vérifiant le code d'état de la réponse
        et si le nombre de places affichées est correct.
        """
        response = server.app.test_client().get('/book/' +
                                                TEST_DICT['competition']
                                                + '/' +
                                                TEST_DICT['name'])
        assert response.status_code == 200
        test_places = "Places available: " + TEST_DICT["numberOfPlaces"]
        assert test_places.encode("utf-8") in response.data

    def test_success_purchase_places(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste la vue purchasePlaces en vérifiant le code de statut de la réponse et
        les points de club restants et les places de compétition restantes.
        """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club=TEST_DICT["name"],
                                                           competition=TEST_DICT["competition"],
                                                           places=TEST_DICT["bookedPlaces"]))
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        remaining_clubs_points = int(TEST_DICT["points"]) - int(TEST_DICT["bookedPlaces"])*3
        remaining_clubs_points = "Points available: " + str(remaining_clubs_points)
        assert remaining_clubs_points.encode("utf-8") in response.data
        remaining_competition_places = int(TEST_DICT["numberOfPlaces"]) - int(TEST_DICT["bookedPlaces"])
        remaining_competition_places = "Number of Places: " + str(remaining_competition_places)
        assert remaining_competition_places.encode("utf-8") in response.data

    def test_success_display_clubs_points(self, fixture_load_clubs):
        """
        Teste si la vue Afficher les points des clubs fonctionne en vérifiant le code d'état de la réponse et
        si le nom du club est inclus dans la réponse.
        """
        response = server.app.test_client().get('/displayClubsPoints')
        assert response.status_code == 200
        assert mock_load_clubs()[0]["name"].encode("utf-8") in response.data

    def test_logout(self):
        """
        Teste si la vue de déconnexion fonctionne en vérifiant le code d'état de la réponse et l'URL
        de la vue redirigée.
        """
        response = server.app.test_client()
        assert response.get('/logout').status_code == 302
        assert b'target URL: <a href="/">/</a>' in response.get('logout').data
