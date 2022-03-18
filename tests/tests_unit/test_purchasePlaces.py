import server
from ..fixtures import fixture_load_clubs, fixture_load_competitions, test_dict


class TestPurchasePlaces:
    """
    Une classe qui rassemble les tests pour la vue purchasePlaces.
    """
    def test_success_purchase_places(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste la vue purchasePlaces en vérifiant le code d'état de la réponse, les points de club restants et les
        places de compétition restantes.
        """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places=test_dict["bookedPlaces"]))
        assert response.status_code == 200
        message = "Great-booking complete!"
        assert message.encode("utf-8") in response.data
        remaining_clubs_points = int(test_dict["points"]) - int(test_dict["bookedPlaces"])*3
        remaining_clubs_points = "Points available: " + str(remaining_clubs_points)
        assert remaining_clubs_points.encode("utf-8") in response.data
        remaining_competition_places = int(test_dict["numberOfPlaces"]) - int(test_dict["bookedPlaces"])
        remaining_competition_places = "Number of Places: " + str(remaining_competition_places)
        assert remaining_competition_places.encode("utf-8") in response.data

    def test_failure_purchase_places(self, fixture_load_clubs, fixture_load_competitions):
        """
        Teste la vue purchasePlaces en vérifiant le message lorsque la compétition est dans le passé.
        """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition="Fall Classic",
                                                           places=test_dict["bookedPlaces"]))
        message = "You can&#39;t book places for a competition that is past."
        assert message.encode("utf-8") in response.data

    def test_failure_purchase_places_2(self, fixture_load_clubs, fixture_load_competitions):
        """
        Tests the purchasePlaces view by checking message when club has not enough points available.
        """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places=str(int(test_dict["points"])//3+1)))
        message = "You don&#39;t have enough points"
        assert message.encode("utf-8") in response.data

    def test_failure_purchase_places_3(self, fixture_load_clubs, fixture_load_competitions):
        """
        Tests the purchasePlaces view by checking message when club tries to book more than 12 places.
        """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club=test_dict["name"],
                                                           competition=test_dict["competition"],
                                                           places="13"))
        message = "You can&#39;t book more than 12 places per competition."
        assert message.encode("utf-8") in response.data
