import json
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

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email')  # utilise get pour éviter KeyError
    if not email:
        flash("Aucun email fourni.")
        return render_template('index.html')

    # recherche du club, renvoie None si pas trouvé
    club = next((c for c in clubs if c['email'] == email), None)

    if not club:
        flash("Email not found.")
        return render_template('index.html')
    
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition_name = request.form['competition']
    club_name = request.form['club']
    competition = next((c for c in competitions if c['name'] == competition_name), None)
    club = next((c for c in clubs if c['name'] == club_name), None)

    if not competition or not club:
        flash("Competition or club not found.")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        flash("Le nombre de places doit être un nombre entier.")
        return render_template('booking.html', club=club, competition=competition)
    placesRequired = int(request.form['places'])

    if int(competition['numberOfPlaces']) <= 0:
        flash("Il n'y a plus de places disponibles dans cette compétition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    elif int(club['booking']) + int(placesRequired) >= 12:
        flash("Vous ne pouvez pas réserver plus de 12 places.")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    elif placesRequired > int(competition['numberOfPlaces']):
        flash("Il n'y a pas assez de places disponibles dans cette compétition.")
        return render_template('booking.html', club=club, competition=competition)
    
    elif placesRequired > int(club['points']):
        flash("Vous n'avez pas assez de points.")
        return render_template('booking.html', club=club, competition=competition)
    
    else:
        club['points'] = int(club['points']) - placesRequired
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['booking'] = int(club['booking']) + placesRequired
        flash(f'Réservation de {placesRequired} places pour {club["name"]} dans la compétition {competition["name"]} réussie!'
              f"Il reste {competition['numberOfPlaces']} places dans {competition['name']}. "
                f"Points restants pour {club['name']} : {club['points']}")
        updateJson('competition.json', 'competitions', competition)
        updateJson('club.json', 'club', club)

        return render_template('welcome.html', club=club, competitions=competitions)


def updateJson(filename, key, data_list):
    with open(filename, 'w') as f: 
        json.dump({key:data_list}, f, indent=4)

# TODO: Add route for points display

@app.route('/')
def clubs_tables():
    clubs = loadClubs()
    return render_template('clubs_tables.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

