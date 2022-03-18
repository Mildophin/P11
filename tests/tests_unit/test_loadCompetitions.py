import json
import server


def test_load_competitions():
    """
    Teste si le chargement des compétitions fonctionne bien
    """
    with open('tests/tests_unit/test_competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
    assert len(listOfCompetitions) == 2
    assert listOfCompetitions[0] == {
            "name": "Spring Festival",
            "date": "2022-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    assert listOfCompetitions == [
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
