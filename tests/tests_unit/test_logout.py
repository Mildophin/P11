import server


def test_logout():
    """
    Teste si la vue logout fonctionne en vérifiant le code d'état de la réponse et l'URL de la vue redirigée.
    """
    response = server.app.test_client()
    assert response.get('/logout').status_code == 302
    assert b'target URL: <a href="/">/</a>' in response.get('logout').data
