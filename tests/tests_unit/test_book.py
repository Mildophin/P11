import server
from ..fixtures import fixture_load_clubs, fixture_load_competitions, test_dict


class TestBook:
    """
    Une classe qui rassemble les tests pour la vue book.
    """
    def test_success_book(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste si la vue book fonctionne en vérifiant le code d'état de la réponse
        et si le nombre de places affichées est correct.
        """
        response = server.app.test_client().get('/book/' +
                                                test_dict['competition']
                                                + '/' +
                                                test_dict['name'])
        assert response.status_code == 200
        test_places = "Places available: " + test_dict["numberOfPlaces"]
        assert test_places.encode("utf-8") in response.data

    def test_failure_book(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste si la vue book fonctionne en vérifiant le code d'état de la réponse d'un chemin d'URL invalide.
        """
        response = server.app.test_client().get('/book/' +
                                                "fake_competition"
                                                + '/' +
                                                test_dict['name'])
        assert response.status_code == 200
        assert b"Something went wrong-please try again" in response.data

    def test_failure_book_2(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste si la vue book fonctionne en vérifiant le code d'état de la réponse d'un chemin d'URL invalide 2.
        """
        response = server.app.test_client().get('/book/' +
                                                test_dict['competition']
                                                + '/' +
                                                "fake_name")
        assert response.status_code == 200
        assert b"Something went wrong-please try again" in response.data
