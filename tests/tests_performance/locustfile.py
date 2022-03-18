from locust import HttpUser, task

EMAIL = "john@simplylift.co"
COMPETITION = "Spring Festival"
CLUB = "Simply Lift"
PLACES = "2"


class ServerTest(HttpUser):

    @task
    def login(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post('/showSummary', data=dict(email=EMAIL))

    @task
    def book(self):
        self.client.get('/book/' + COMPETITION + '/' + CLUB)

    @task
    def purchasePlaces(self):
        self.client.post('/purchasePlaces', data=dict(club=CLUB,
                                                      competition=COMPETITION,
                                                      places=PLACES))

    @task
    def displayClubsPoints(self):
        self.client.get('/displayClubsPoints')

    @task
    def logout(self):
        self.client.get('/logout')
