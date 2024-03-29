from main import app, db
from main.models import User
from main.forms import RegistrationForm, LoginForm, NaamGegevensForm, AdresGegevensForm, NieuwWachtwoordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from main.checks import check_profiel, check_Unique, check_and_store_wachtwoord

@app.route('/logout') # Logt de gebruiker uit
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('login'))

@app.route('/vragenlijst')
def vragenlijst():
    return render_template('vragenlijst.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user is not None:
            if user.check_password(form.wachtwoord.data):

                login_user(user)
                flash('Logged in successfully.')

                next = request.args.get('next')

                if next == None or not next[0] == '/':
                    next = url_for('profiel')
                flash('Inloggen gelukt')
                return redirect(next)
        else:
            flash('Inloggen mislukt, probeer opnieuw.')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        try:
            gebruikersnaam = request.form['gebruikersnaam']
            email = request.form['email'].lower()
            geslacht = request.form['geslacht']
            telefoon = request.form['telefoon']
            password = request.form['wachtwoord']
            nieuwe_user = User(gebruikersnaam=gebruikersnaam, email=email, geslacht=geslacht, telefoon=telefoon, 
                            password=password, voornaam=None, achternaam=None, adres=None, stad=None, taal=None, land=None)
            db.session.add(nieuwe_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            flash('Gebruikersnaam of E-Mail al in gebruik!')
    return render_template('register.html', form=form)

@app.route('/profiel', methods=['GET', 'POST'])
@login_required
def profiel():

    user = User.query.filter_by(id=current_user.get_id()).first()
    naamGegevensForm = NaamGegevensForm()
    adresGegevensForm = AdresGegevensForm()
    nieuwWachtwoordForm = NieuwWachtwoordForm()
    # Check of de request methode "POST" is
    if request.method == "POST":
        
        # Aanpassingen inventariseren
        gebruikersnaam = request.form.get('gebruikersnaam')
        email = request.form.get('email')
        voornaam = request.form.get('voornaam')
        achternaam = request.form.get('achternaam')
        adres = request.form.get('adres')
        stad = request.form.get('stad')
        land = request.form.get('land')
        taal = request.form.get('engels')
        telefoon = request.form.get('telefoon')
        wachtwoord = request.form.get('wachtwoord')

        titels = ['gebruikersnaam', 'email', 'voornaam', 'achternaam', 'adres', 'stad', 'land', 'taal', 'telefoon']
        waardes = [gebruikersnaam, email, voornaam, achternaam, adres, stad, land, taal, telefoon]

        # Check of gebruikersnaam en email bestaat 
        gebruikersnaam_bestaat = check_Unique(User, 'gebruikersnaam', gebruikersnaam)
        email_bestaat = check_Unique(User, 'email', email)
        check_and_store_wachtwoord(user, wachtwoord)

        if gebruikersnaam_bestaat:
            return redirect(url_for('profiel')), flash('Gebruikersnaam bestaat al')

        if email_bestaat:
            return redirect(url_for('profiel')), flash('Email bestaat al')


        # Check waardes en data
        for i, j in zip(titels, waardes):
            check_profiel(user, i, j)
        

    gebruikersnaam = user.gebruikersnaam
    email = user.email
    voornaam = user.voornaam
    achternaam = user.achternaam
    email = user.email
    adres = user.adres
    stad = user.stad
    land = user.land
    telefoon = user.telefoon

    return render_template('profiel.html', gebruikersnaam=gebruikersnaam, email=email, voornaam=voornaam, achternaam=achternaam,
                            adres=adres, stad=stad, land=land, telefoon=telefoon, naamGegevensForm=naamGegevensForm, adresGegevensForm=adresGegevensForm, nieuwWachtwoordForm=nieuwWachtwoordForm)


if __name__ == '__main__':
    app.run(debug=True)