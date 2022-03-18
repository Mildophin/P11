import server


def test_index():
    """
    Teste si la vue de l'index fonctionne en vérifiant le code d'état de la réponse.
    """
    response = server.app.test_client()
    assert response.get('/').status_code == 200
