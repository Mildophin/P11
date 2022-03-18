import server
from ..fixtures import mock_load_clubs, fixture_load_clubs


class TestDisplayClubsPoints:
    """
    Une classe qui rassemble les tests pour la vue displayClubsPoints.
    """
    def test_success_display_clubs_points(self, fixture_load_clubs):
        """
        Teste si la vue displayClubsPoints fonctionne en vérifiant le code d'état de la réponse et si le
        nom du club est inclus dans la réponse et si le nom du club est inclus dans la réponse.
        """
        response = server.app.test_client().get('/displayClubsPoints')
        assert response.status_code == 200
        assert mock_load_clubs()[0]["name"].encode("utf-8") in response.data
