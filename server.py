import json
from datetime import datetime

from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    """
    Route pour la connexion des utilisateurs.
    :return: un template
    """
    # Debug bug/Entrer un email inconnu fait crasher l'application
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions)
    except IndexError:
        message = "Sorry, that email wasn't found."
        flash(message, 'error')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    availablePoints = int(club.get('points', None))
    competitionDate = datetime.strptime(competition['date'],
                                                 '%Y-%m-%d %H:%M:%S')
    # Debug bug/Les clubs ne peuvent pas utiliser plus de points que ce qu'ils ont
    if placesRequired > availablePoints:
        message = f"You don't have enough points to book {placesRequired} places."
        flash(message, 'error')
        return render_template('welcome.html', club=club, competitions=competitions)
    # Debug bug/Les clubs ne peuvent pas réserver plus de 12 places par compétition
    elif placesRequired > 12:
        message = "You can't book more than 12 places per competition."
        flash(message, 'error')
        return render_template('welcome.html', club=club, competitions=competitions)
        # Debug bug/Réservation pour des compétitions passées
    elif competitionDate < datetime.now():
        message = "You can't book places for a competition that is past."
        flash(message, 'error')
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    # Debug bug/Mise a jour des points non fonctionnel
    club['points'] = int(club['points'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, availablePoints=availablePoints)


@app.route('/displayClubsPoints')
def displayClubsPoints():
    return render_template('display_clubs_points.html', clubs=clubs, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
