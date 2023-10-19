import sqlalchemy
from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user,  LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField,TextAreaField
from wtforms.validators import InputRequired,DataRequired, Length, ValidationError,EqualTo, NumberRange
from wtforms.validators import Email
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint
import plotly.graph_objects as go
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oaza.db'
app.config['SECRET_KEY'] = 'tojestsekretkey'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Uzytkownicy.query.get(int(user_id))

# uzytkownik
class Uzytkownicy(db.Model, UserMixin):
    __tablename__ = 'uzytkownicy'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(20), nullable=False)
    nazwisko = db.Column(db.String(40), nullable=False)
    haslo = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    druzyny = db.relationship('Druzyny', backref='uzytkownik', uselist=False)
    events = db.relationship('Event', backref='uzytkownik', lazy=True)

#kontakt
class Kontakt(db.Model,UserMixin):
    __tablename__ = 'kontakt'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(100), nullable=False)
    nazwisko = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    wiadomosc = db.Column(db.Text, nullable=False)


# druzyna
class Druzyny(db.Model, UserMixin):
    __tablename__ = 'druzyny'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'), unique=True)
    zawodnicy = db.relationship('Player', backref='druzyna')

# zawodnicy
class Player(db.Model, UserMixin):
    __tablename__ = 'zawodnicy'
    id = db.Column(db.Integer, primary_key=True)
    imie = db.Column(db.String(50), nullable=False)
    nazwisko = db.Column(db.String(50), nullable=False)
    wzrost = db.Column(db.Integer, nullable=False)
    waga = db.Column(db.Integer, nullable=False)
    pozycja = db.Column(db.String(20), nullable=False)
    szybkosc = db.Column(db.Integer, nullable=False)
    sila = db.Column(db.Integer, nullable=False)
    drybling = db.Column(db.Integer, nullable=False)
    strzal = db.Column(db.Integer, nullable=False)
    defensywa = db.Column(db.Integer, nullable=False)
    podania = db.Column(db.Integer, nullable=False)
    noga = db.Column(db.String(20), nullable=False)
    druzyna_id = db.Column(db.Integer, db.ForeignKey('druzyny.id'), nullable=False)
    
class Event(db.Model,UserMixin):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    all_day = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('uzytkownicy.id'), unique=True)


class Pozycja:
        def __init__(self, pozycja,zawodnik, ocena):
            self.pozycja = pozycja
            self.ocena = []
            self.zawodnik = []

pozycje = [
        Pozycja('Bramkarz',None,0),
        Pozycja('Lewy obrońca', None,0),
        Pozycja('Prawy obrońca', None,0),
        Pozycja('Środkowy obrońca', None,0),
        Pozycja('Prawy pomocnik', None,0),
        Pozycja('Środkowy pomocnik', None,0),
        Pozycja('Ofensywny pomocnik', None,0),
        Pozycja('Defensywny pomocnik', None,0),
        Pozycja('Lewy pomocnik', None,0),
        Pozycja('Lewy skrzydłowy', None,0),
        Pozycja('Prawy skrzydłowy', None,0),
        Pozycja('Napastnik', None,0)
    ]

def reset_pozycja():
        pozycje.clear()
        pozycje.append(Pozycja('Bramkarz',None,0))
        pozycje.append(Pozycja('Lewy obrońca', None,0))
        pozycje.append(Pozycja('Prawy obrońca', None,0))
        pozycje.append(Pozycja('Środkowy obrońca', None,0))
        pozycje.append(Pozycja('Prawy pomocnik', None,0))
        pozycje.append(Pozycja('Środkowy pomocnik', None,0))
        pozycje.append(Pozycja('Ofensywny pomocnik', None,0))
        pozycje.append(Pozycja('Defensywny pomocnik', None,0))
        pozycje.append(Pozycja('Lewy pomocnik', None,0))
        pozycje.append(Pozycja('Lewy skrzydłowy', None,0))
        pozycje.append(Pozycja('Prawy skrzydłowy', None,0))
        pozycje.append(Pozycja('Napastnik', None,0))

def pobierz_zawodnikow(klub_obecny):
    zawodnicy = Player.query.filter_by(druzyna_id=klub_obecny).all()
    lista_zawodnikow = []
    for player in zawodnicy:
        player_dict = {
            'Imie': player.imie +' '+ player.nazwisko,
            'Wzrost': player.wzrost,
            'Pozycja': player.pozycja,
            'Sila': player.sila,
            'Szybkosc': player.szybkosc,
            'Drybling': player.drybling,
            'Defensywa': player.defensywa,
            'Podania': player.podania,
            'Strzaly': player.strzal,
            'Preferowana_Noga': player.noga
        }
        lista_zawodnikow.append(player_dict)

    return lista_zawodnikow


def znajdz_najlepszego_bramkarza(zawodnicy):
     naj_bramkarz = None
     naj_bramkarz_score = 0
     reszta=[]
    
     waga_defensywa = 0.2
     waga_szybkosc = 0.1
     waga_podania = 0.15
     waga_drybling = 0.0
     waga_sila = 0.1
     waga_strzaly = 0.0

     for player in zawodnicy:
        if player['Pozycja'] == "BR":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Wzrost'] > 185:
               score += 5
            if score > naj_bramkarz_score:
                if naj_bramkarz is not None:
                    reszta.append(naj_bramkarz)
                naj_bramkarz = player
                naj_bramkarz_score = score
            else:
                reszta.append(player)
     
     if naj_bramkarz == None:
         return None
     naj_bramkarz['score'] = (naj_bramkarz_score)

     for player  in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

     return naj_bramkarz, reszta

def znajdz_najlepszego_obronce(zawodnicy):
     naj_obronca = None
     naj_obronca_score = 0
     reszta=[]
    
     waga_defensywa = 0.3
     waga_szybkosc = 0.1
     waga_podania = 0.1
     waga_drybling = 0.05
     waga_sila = 0.2
     waga_strzaly = 0.05

     for player in zawodnicy:
        if player['Pozycja'] == "ŚO":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * 
                          waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Wzrost'] > 180:
               score += 5
            if score > naj_obronca_score:
                if naj_obronca is not None:
                    reszta.append(naj_obronca)
                naj_obronca = player
                naj_obronca_score = score
            else:
                reszta.append(player)
     
     if naj_obronca == None:
         return None
     naj_obronca['score'] = (naj_obronca_score)

     for player  in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * 
                                 waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

     return naj_obronca, reszta

def znajdz_lewego_bocznego(zawodnicy):
    naj_lewyOB = None
    naj_lewyOB_score = 0
    reszta = []

    waga_defensywa = 0.25
    waga_szybkosc = 0.1
    waga_podania = 0.1
    waga_drybling = 0.05
    waga_sila = 0.1
    waga_strzaly = 0.0

    for player in zawodnicy:
        if player['Pozycja'] == "LO":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'lewa':
               score += 5 
            if score > naj_lewyOB_score:
                if naj_lewyOB is not None:
                    reszta.append(naj_lewyOB)
                naj_lewyOB = player
                naj_lewyOB_score = score
            else:
                reszta.append(player)
    if naj_lewyOB == None:
         return None
    naj_lewyOB['score'] = (naj_lewyOB_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

    return naj_lewyOB, reszta

def znajdz_prawego_bocznego(zawodnicy):

    naj_prawyOB = None
    naj_prawyOB_score = 0
    reszta = []

    waga_defensywa = 0.25
    waga_szybkosc = 0.1
    waga_podania = 0.1
    waga_drybling = 0.05
    waga_sila = 0.1
    waga_strzaly = 0.0

    for player in zawodnicy:
        if player['Pozycja'] =="PO":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'prawa':
               score += 5
            if score > naj_prawyOB_score:
                if naj_prawyOB is not None:
                    reszta.append(naj_prawyOB)
                naj_prawyOB = player
                naj_prawyOB_score = score
            else:
                reszta.append(player)
    if naj_prawyOB == None:
         return None
    naj_prawyOB['score'] = (naj_prawyOB_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

    return naj_prawyOB, reszta

def spd(zawodnicy):
    naj_spd = None
    naj_spd_score = 0
    reszta = []

    waga_defensywa = 0.2
    waga_szybkosc = 0.15
    waga_podania = 0.2
    waga_drybling = 0.15
    waga_sila = 0.1
    waga_strzaly = 0.1

    for player in zawodnicy:
        if player['Pozycja'] =="ŚPD":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'obunożny':
               score += 5
            if score > naj_spd_score:
                if naj_spd is not None:
                    reszta.append(naj_spd)
                naj_spd = player
                naj_spd_score = score
            else:
                reszta.append(player)

    if naj_spd == None:
         return None
    naj_spd['score'] = (naj_spd_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
    return naj_spd, reszta

def sp(zawodnicy):
    naj_sp = None
    naj_sp_score = 0
    reszta = []

    waga_defensywa = 0.2
    waga_szybkosc = 0.15
    waga_podania = 0.2
    waga_drybling = 0.2
    waga_sila = 0.1
    waga_strzaly = 0.15

    for player in zawodnicy:
        if player ['Pozycja'] =="ŚP":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'obunożny':
               score += 5
            if score > naj_sp_score:
                if naj_sp is not None:
                    reszta.append(naj_sp)
                naj_sp = player
                naj_sp_score = score
            else:
                reszta.append(player)

    if naj_sp == None:
         return None
    naj_sp['score'] = (naj_sp_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

    return naj_sp, reszta

def spo(zawodnicy):
    naj_spo = None
    naj_spo_score = 0
    reszta = []

    waga_defensywa = 0.1
    waga_szybkosc = 0.1
    waga_podania = 0.15
    waga_drybling = 0.2
    waga_sila = 0.05
    waga_strzaly = 0.4

    for player in zawodnicy:
        if player ['Pozycja'] =="ŚPO":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + 
                          player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'obunożny':
               score += 5
            if score > naj_spo_score:
                if naj_spo is not None:
                    reszta.append(naj_spo)
                naj_spo = player
                naj_spo_score = score
            else:
                reszta.append(player)
    if naj_spo == None:
         return None
    naj_spo['score'] = (naj_spo_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + 
                                 player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

    return naj_spo, reszta

def pp(zawodnicy):
    naj_pp = None
    naj_pp_score = 0
    reszta = []

    waga_defensywa = 0.15
    waga_szybkosc = 0.15
    waga_podania = 0.2
    waga_drybling = 0.25
    waga_sila = 0.05
    waga_strzaly = 0.1

    for player in zawodnicy:
        if player ['Pozycja'] =="PP":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'prawa':
               score += 5
            if score > naj_pp_score:
                if naj_pp is not None:
                    reszta.append(naj_pp)
                naj_pp = player
                naj_pp_score = score
            else:
                reszta.append(player)
    if naj_pp == None:
         return None
    naj_pp['score'] = (naj_pp_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
    return naj_pp, reszta

def lp(zawodnicy):

    naj_lp = None
    naj_lp_score = 0
    reszta = []

    waga_defensywa = 0.15
    waga_szybkosc = 0.15
    waga_podania = 0.2
    waga_drybling = 0.25
    waga_sila = 0.05
    waga_strzaly = 0.1

    for player in zawodnicy:
        if player ['Pozycja'] =="LP":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'lewa':
               score += 5
            if score > naj_lp_score:
                if naj_lp is not None:
                    reszta.append(naj_lp)
                naj_lp = player
                naj_lp_score = score
            else:
                reszta.append(player)

    if naj_lp == None:
         return None
    naj_lp['score'] = (naj_lp_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

    return naj_lp, reszta

# atak
def ls(zawodnicy):
    naj_ls = None
    naj_ls_score = 0
    reszta = []

    waga_defensywa = 0.1
    waga_szybkosc = 0.25
    waga_podania = 0.15
    waga_drybling = 0.25
    waga_sila = 0.05
    waga_strzaly = 0.2

    for player in zawodnicy:
        if player ['Pozycja'] =="LS":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'lewa':
               score += 5
            if score > naj_ls_score:
                if naj_ls is not None:
                    reszta.append(naj_ls)
                naj_ls = player
                naj_ls_score = score
            else:
                reszta.append(player)
    if naj_ls == None:
         return None
    naj_ls['score'] = (naj_ls_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

    return naj_ls, reszta

def ps(zawodnicy):
    naj_ps = None
    naj_ps_score = 0
    reszta = []

    waga_defensywa = 0.1
    waga_szybkosc = 0.25
    waga_podania = 0.15
    waga_drybling = 0.25
    waga_sila = 0.05
    waga_strzaly = 0.2

    for player in zawodnicy:
        if player ['Pozycja'] =="PS":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'prawa':
               score += 5
            if score > naj_ps_score:
                if naj_ps is not None:
                    reszta.append(naj_ps)
                naj_ps = player
                naj_ps_score = score
            else:
                reszta.append(player)
    if naj_ps == None:
         return None
    naj_ps['score'] = (naj_ps_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)

    return naj_ps, reszta


def n(zawodnicy):
    naj_n = None
    naj_n_score = 0
    reszta = []
    waga_defensywa = 0.1
    waga_szybkosc = 0.25
    waga_podania = 0.1
    waga_drybling = 0.2
    waga_sila = 0.1
    waga_strzaly = 0.25

    for player in zawodnicy:
        if player ['Pozycja'] =="N":
            score = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
            if player ['Preferowana_Noga'] == 'obunożny':
               score += 5
            if score > naj_n_score:
                if naj_n is not None:
                    reszta.append(naj_n)
                naj_n = player
                naj_n_score = score
            else:
                reszta.append(player)

    if naj_n == None:
         return None
    naj_n['score'] = (naj_n_score)

    for player in reszta:
         player['score'] = round(player['Defensywa'] * waga_defensywa + player['Szybkosc'] * waga_szybkosc + player['Podania'] * waga_podania  + player['Drybling'] * waga_drybling + player['Sila'] * waga_sila + player['Strzaly'] * waga_strzaly,2)
    return naj_n, reszta



class Oceny:
    def __init__(self,zawodnik,ocena) -> None:
        self.zawodnik = zawodnik
        self.ocena = ocena
        
     
def okresl_pozycje2():

    klub_obecny = current_user.druzyny.id if current_user.druzyny else None
    zawodnicy = pobierz_zawodnikow(klub_obecny)
    if len(zawodnicy)>=12:
        oceny = []
        for zawodnik in zawodnicy:
            waga_defensywa = 0.1
            waga_szybkosc = 0.25
            waga_podania = 0.1
            waga_drybling = 0.2
            waga_sila = 0.1
            waga_strzaly = 0.25
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling 
                          + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'obunożny':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Napastnik":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()
        
        for zawodnik in zawodnicy:
            waga_defensywa = 0.1
            waga_szybkosc = 0.25
            waga_podania = 0.15
            waga_drybling = 0.25
            waga_sila = 0.05
            waga_strzaly = 0.2
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'prawa':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Prawy skrzydłowy":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.1
            waga_szybkosc = 0.25
            waga_podania = 0.15
            waga_drybling = 0.25
            waga_sila = 0.05
            waga_strzaly = 0.2
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'lewa':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Lewy skrzydłowy":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()
# pom
        for zawodnik in zawodnicy:
            waga_defensywa = 0.2
            waga_szybkosc = 0.15
            waga_podania = 0.2
            waga_drybling = 0.2
            waga_sila = 0.1
            waga_strzaly = 0.15
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'obunożny':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Środkowy pomocnik":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.15
            waga_szybkosc = 0.15
            waga_podania = 0.2
            waga_drybling = 0.25
            waga_sila = 0.05
            waga_strzaly = 0.1
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'prawa':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Prawy pomocnik":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.15
            waga_szybkosc = 0.15
            waga_podania = 0.2
            waga_drybling = 0.25
            waga_sila = 0.05
            waga_strzaly = 0.1
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'lewa':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Lewy pomocnik":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.2
            waga_szybkosc = 0.15
            waga_podania = 0.2
            waga_drybling = 0.15
            waga_sila = 0.1
            waga_strzaly = 0.1
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'obunożny':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Defensywny pomocnik":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.1
            waga_szybkosc = 0.1
            waga_podania = 0.15
            waga_drybling = 0.2
            waga_sila = 0.05
            waga_strzaly = 0.4
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'obunożny':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Ofensywny pomocnik":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.3
            waga_szybkosc = 0.1
            waga_podania = 0.1
            waga_drybling = 0.05
            waga_sila = 0.2
            waga_strzaly = 0.05
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Wzrost'] > 180:
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Środkowy obrońca":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.25
            waga_szybkosc = 0.1
            waga_podania = 0.1
            waga_drybling = 0.05
            waga_sila = 0.1
            waga_strzaly = 0.05
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'prawa':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Prawy obrońca":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.25
            waga_szybkosc = 0.1
            waga_podania = 0.1
            waga_drybling = 0.05
            waga_sila = 0.1
            waga_strzaly = 0.05
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Preferowana_Noga'] == 'Lewa':
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Lewy obrońca":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()

        for zawodnik in zawodnicy:
            waga_defensywa = 0.2
            waga_szybkosc = 0.1
            waga_podania = 0.15
            waga_drybling = 0.0
            waga_sila = 0.1
            waga_strzaly = 0.0
            ocena = round(zawodnik['Defensywa'] * waga_defensywa + zawodnik['Szybkosc'] * waga_szybkosc + zawodnik['Podania'] * waga_podania  + zawodnik['Drybling'] * waga_drybling + zawodnik['Sila'] * waga_sila + zawodnik['Strzaly'] * waga_strzaly,2)
            if zawodnik['Wzrost'] > 185:
                ocena += 5
            oceny.append(Oceny(zawodnik,ocena))
        oceny.sort(key=lambda z: z.ocena, reverse=True)
        for x in pozycje:
            if x.pozycja == "Bramkarz":
                x.zawodnik.append(oceny[0].zawodnik) 
                x.ocena.append(oceny[0].ocena)
                x.zawodnik.append(oceny[1].zawodnik)
                x.ocena.append(oceny[1].ocena)
                x.zawodnik.append(oceny[2].zawodnik)
                x.ocena.append(oceny[2].ocena)
                break
        oceny.clear()     


# formularz rejestacji
class RejestracjaForm(FlaskForm):
    imie = StringField('Imię', validators=[InputRequired(), Length(min=2, max=20)])
    nazwisko = StringField('Nazwisko', validators=[InputRequired(), Length(min=2, max=40)])
    email = StringField('Adres email', validators=[InputRequired(), Length(max=80), Email()])
    haslo = PasswordField('Hasło', validators=[InputRequired(), Length(min=8, max=80)])
    powtorz_haslo = PasswordField('Powtórz hasło', validators=[InputRequired(), EqualTo('haslo', message='Hasła nie są identyczne')])
    submit = SubmitField('Zarejestruj się')

class KontaktForm(FlaskForm):
    imie = StringField('Imię', validators=[DataRequired()])
    nazwisko = StringField('Nazwisko', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    wiadomosc = TextAreaField('Wiadomość', validators=[DataRequired()])
    submit = SubmitField('Wyślij')

# formularz tworzenia druzyny
class TeamForm(FlaskForm):
    nazwa = StringField('Nazwa drużyny')
    submit = SubmitField('Utwórz drużynę')

class ZmianaNazwy(FlaskForm):
    nowa_nazwa = StringField('Wpisz nową nazwę')
    submit = SubmitField('Zmień nazwe')

def validate_email(self, email):
        uzytkownik = Uzytkownicy.query.filter_by(email=email.data).first()
        if uzytkownik is not None:
            raise ValidationError('Użytkownik o takim adresie email już istnieje.')
     
# formularz logowania
class Login(FlaskForm):
    email = StringField('Adres email', validators=[InputRequired(), Length(max=80), Email()])
    haslo = PasswordField('Hasło', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Zaloguj')

#formularz dodawania zawodnika beta
class AddPlayerForm(FlaskForm):
    imie = StringField('Imię', validators=[DataRequired(), Length(max=50)])
    nazwisko = StringField('Nazwisko', validators=[DataRequired(), Length(max=50)])
    wzrost = IntegerField('Wzrost (cm)', validators=[DataRequired(), NumberRange(min=1)])
    waga = IntegerField('Waga (kg)', validators=[DataRequired(), NumberRange(min=1)])
    pozycja = SelectField('Pozycja', choices=[
        ('', 'Wybierz pozycję'),
        ('BR', 'BR'),
        ('ŚO', 'ŚO'),
        ('LO', 'LO'),
        ('PO', 'PO'),
        ('ŚP', 'ŚP'),
        ('LP', 'LP'),
        ('PP', 'PP'),
        ('ŚPO', 'ŚPO'),
        ('ŚPD', 'ŚPD'),
        ('LS', 'LS'),
        ('PS', 'PS'),
        ('N', 'N')
    ], validators=[DataRequired()])
    szybkosc = IntegerField('Szybkość', validators=[DataRequired(), NumberRange(min=1)])
    sila = IntegerField('Siła', validators=[DataRequired(), NumberRange(min=1)])
    drybling = IntegerField('Drybling', validators=[DataRequired(), NumberRange(min=1)])
    strzal = IntegerField('Strzał', validators=[DataRequired(), NumberRange(min=1)])
    defensywa = IntegerField('Defensywa', validators=[DataRequired(), NumberRange(min=1)])
    podania = IntegerField('Podania', validators=[DataRequired(), NumberRange(min=1)])
    noga = SelectField('Noga wiodąca', choices=[
        ('', 'Wybierz nogę wiodącą'),
        ('prawa', 'Prawo nożny'),
        ('lewa', 'Lewo nożny'),
        ('obunożny', 'Obunożny')
    ], validators=[DataRequired()])
    submit = SubmitField('Dodaj zawodnika')

class PozycjeObronne(FlaskForm):
    pozycje = SelectField('Pozycja', choices=[('','Wybierz Pozycje'),('ŚO', 'ŚO'), ('LO', 'LO'), ('PO', 'PO'), ('BR', 'BR')])
    guzik = SubmitField('Wyszukaj zawodnika')

class Pomoc(FlaskForm):
    pozycje2 = SelectField('Pozycja', choices=[('','Wybierz Pozycje'),('ŚPD', 'ŚPD'), ('ŚP', 'ŚP'), ('ŚPO', 'ŚPO'), ('PP', 'PP'), ('LP', 'LP')])
    guzik2 = SubmitField('Wyszukaj zawodnika')
class Atak(FlaskForm):
    pozycje3 = SelectField('Pozycja', choices=[('','Wybierz Pozycje'),('N', 'N'), ('PS', 'PS'), ('LS', 'LS')])
    guzik3 = SubmitField('Wyszukaj zawodnika')

# routy
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    form = KontaktForm()

    if form.validate_on_submit():
        imie = form.imie.data
        nazwisko = form.nazwisko.data
        email = form.email.data
        wiadomosc = form.wiadomosc.data

        dodaj_kontakt = Kontakt(imie=imie, nazwisko=nazwisko, email=email, wiadomosc=wiadomosc)
        db.session.add(dodaj_kontakt)
        db.session.commit()

        return redirect(url_for('kontakt'))

    return render_template('kontakt.html', form=form)

@app.route('/onas')
def onas():
    return render_template('onas.html')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
     return render_template('admin.html')

@app.route('/harmonogram', methods=['GET', 'POST'])
@login_required
def calendar():
    return render_template('harmonogram.html')

@app.route('/opcje', methods=['GET', 'POST'])
@login_required
def opcje():
     
    klub_obecny = current_user.druzyny.id if current_user.druzyny else None
    zawodnicy = pobierz_zawodnikow(klub_obecny)
    form = ZmianaNazwy()

    if form.validate_on_submit():
        nowa_nazwa = form.nowa_nazwa.data

        takisam_team = Druzyny.query.filter_by(nazwa=nowa_nazwa).first()
        if takisam_team is not None:
            flash('Nazwa drużyny jest już zajęta. Proszę wybrać inną nazwę.')
            return redirect(url_for('admin'))

        if current_user.druzyny is None:
            flash('Nie posiadasz jeszcze drużyny. Najpierw utwórz drużynę.')
            return redirect(url_for('admin'))

        druzyna = current_user.druzyny
        druzyna.nazwa = nowa_nazwa
        db.session.commit()
        flash('Nazwa drużyny została zmieniona.')
        return redirect(url_for('admin'))

    return render_template('opcje.html', zawodnicy=zawodnicy, form=form)


@app.route("/get-events", methods=["GET"])
@login_required
def get_events():
    events = Event.query.filter_by(user_id=current_user.id).all()
    event_data = []
    for event in events:
        event_data.append({
            "id": event.id,
            "title": event.title,
            "start": event.start.isoformat(),
            "end": event.end.isoformat(),
            "allDay": event.all_day
        })

    return jsonify(events=event_data)


@app.route("/events", methods=["POST"])
@login_required
def create_event():
    event_data = request.get_json()
    title = event_data["title"]
    start = datetime.fromisoformat(event_data["start"])
    end = datetime.fromisoformat(event_data["end"])
    all_day = event_data["allDay"]

    event = Event(title=title, start=start, end=end, all_day=all_day, user_id=current_user.id)
    db.session.add(event)
    db.session.commit()

    return jsonify(id=event.id)


@app.route("/events/<int:event_id>", methods=["PUT"])
@login_required
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Nie znaleziono zdarzenia"})

    event_data = request.get_json()
    title = event_data["title"]
    start = datetime.fromisoformat(event_data["start"])
    end = datetime.fromisoformat(event_data["end"])
    all_day = event_data["allDay"]

    event.title = title
    event.start = start
    event.end = end
    event.all_day = all_day

    db.session.commit()

    return jsonify({"message": "Zdarzenie zaaktualizowane"})


@app.route("/events/<int:event_id>", methods=["DELETE"])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Nie znaleziono zdarzenia"})

    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Usunieto zdarzenie"})


@app.route('/boisko', methods=['GET', 'POST'])
@login_required
def boisko():
     return render_template('taktyka.html')

@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    klub_obecny = current_user.druzyny.id if current_user.druzyny else None
    zawodnicy = pobierz_zawodnikow(klub_obecny)

#szybkosc
    posortowani_zawodnicy = sorted(zawodnicy, key=lambda x: x['Szybkosc'], reverse=True)

    nazwiska = [f"{zawodnik['Imie']}" for zawodnik in posortowani_zawodnicy]
    szybkosc = [zawodnik['Szybkosc'] for zawodnik in posortowani_zawodnicy]

    fig = go.Figure(data=[go.Bar(x=nazwiska , y=szybkosc)])
    fig.update_layout(title='Najszybsi zawodnicy', xaxis_title='Zawodnik', yaxis_title='Szybkość')
    
# sila
    sort_sila = sorted(zawodnicy, key=lambda x: x['Sila'], reverse=True)

    nazwisko_sila = [f"{zawodnik['Imie']} " for zawodnik in sort_sila]
    sila = [zawodnik['Sila'] for zawodnik in sort_sila]

    fig_sila = go.Figure(data=[go.Bar(x=nazwisko_sila , y=sila)])
    fig_sila.update_layout(title='Najsilniejsi zawodnicy', xaxis_title='Zawodnik', yaxis_title='Sila')

# strzelcy
    sort_strzal = sorted(zawodnicy, key=lambda x: x['Strzaly'], reverse=True)

    nazwisko_strzal = [f"{zawodnik['Imie']}" for zawodnik in sort_strzal]
    strzal = [zawodnik['Strzaly'] for zawodnik in sort_strzal]

    fig_strzal = go.Figure(data=[go.Bar(x=nazwisko_strzal , y=strzal)])
    fig_strzal.update_layout(title='Najlepsze strzały', xaxis_title='Zawodnik', yaxis_title='Strzały')

#średnia wieku
    suma_wzrostu = sum(zawodnik["Wzrost"] for zawodnik in zawodnicy)
    sredni_wzrost = round(suma_wzrostu / len(zawodnicy),2) if current_user.druzyny else None
    fig_wzrost = go.Figure(data=go.Bar(x=["Średni wzrost"], y=[sredni_wzrost]))
    fig_wzrost.update_layout(title="Średni wzrost zawodników", yaxis_title="Wzrost (cm)")

# Konwertowanie wykresu na HTML
    wykres_html = fig.to_html(full_html=False)
    wykres_sila = fig_sila.to_html(full_html=False)
    wykres_strzal = fig_strzal.to_html(full_html=False)
    wykres_wzrost = fig_wzrost.to_html(full_html=False)

    return render_template('statystyki.html',wykres_wzrost=wykres_wzrost,wykres_html=wykres_html,wykres_sila=wykres_sila,wykres_strzal=wykres_strzal)


@app.route('/matchhim', methods=['GET', 'POST'])
@login_required
def matchhim():

      form=PozycjeObronne()
      pom = Pomoc()
      ata = Atak()

      klub_obecny = current_user.druzyny.id if current_user.druzyny else None
      zawodnicy = pobierz_zawodnikow(klub_obecny)

      bram = znajdz_najlepszego_bramkarza(zawodnicy)
      obr = znajdz_najlepszego_obronce(zawodnicy)
      lewy = znajdz_lewego_bocznego(zawodnicy)
      prawy = znajdz_prawego_bocznego(zawodnicy)
      pomd = spd(zawodnicy)
      poms = sp(zawodnicy)
      pomo = spo(zawodnicy)
      ppom = pp(zawodnicy)
      lpom = lp(zawodnicy)
      lsa = ls(zawodnicy)
      psa = ps(zawodnicy)
      na = n(zawodnicy)

      naj_bramkarz = None
      naj_obronca = None
      naj_lewyOB = None
      naj_prawyOB = None
      naj_spd = None
      naj_sp = None
      naj_spo = None
      naj_pp = None
      naj_lp = None
      naj_ls = None
      naj_ps = None
      naj_n = None
      reszta=[]

      if form.validate_on_submit():
        selected_position = form.pozycje.data

        if selected_position == 'ŚO':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_obronca, reszta = znajdz_najlepszego_obronce(zawodnicy)

        if selected_position == 'LO':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_lewyOB, reszta = znajdz_lewego_bocznego(zawodnicy)

        if selected_position == 'PO':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_prawyOB, reszta = znajdz_prawego_bocznego(zawodnicy)

        if selected_position == 'BR':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_bramkarz, reszta = znajdz_najlepszego_bramkarza(zawodnicy)

        return jsonify(naj_obronca=naj_obronca, naj_lewyOB=naj_lewyOB, reszta=reszta, naj_prawyOB=naj_prawyOB, naj_bramkarz=naj_bramkarz)

      if pom.validate_on_submit():
        selected_position = pom.pozycje2.data

        if selected_position == 'ŚPD':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_spd, reszta = spd(zawodnicy)

        if selected_position == 'ŚP':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_sp, reszta = sp(zawodnicy)

        if selected_position == 'ŚPO':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_spo, reszta = spo(zawodnicy)

        if selected_position == 'PP':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_pp, reszta = pp(zawodnicy) 

        if selected_position == 'LP':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_lp, reszta = lp(zawodnicy) 


        return jsonify(naj_spd=naj_spd, reszta=reszta, naj_sp=naj_sp, naj_spo=naj_spo, naj_pp=naj_pp, naj_lp=naj_lp)
      
      if ata.validate_on_submit():
        selected_position = ata.pozycje3.data

        if selected_position == 'LS':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_ls, reszta = ls(zawodnicy)

        if selected_position == 'PS':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_ps, reszta = ps(zawodnicy)

        if selected_position == 'N':
            klub_obecny = current_user.druzyny.id
            zawodnicy = pobierz_zawodnikow(klub_obecny)
            naj_n, reszta = n(zawodnicy)


        return jsonify(naj_ls=naj_ls,naj_ps=naj_ps,naj_n=naj_n, reszta=reszta)
     
      reset_pozycja()
      okresl_pozycje2()

      return render_template('match.html',pozycje=pozycje,zawodnicy=zawodnicy,na=na,psa=psa,lsa=lsa,lpom=lpom,ppom=ppom,pomo=pomo,poms=poms,pomd=pomd,obr=obr,lewy=lewy,prawy=prawy, form=form, naj_obronca=naj_obronca,naj_lewyOB=naj_lewyOB, reszta=reszta, naj_prawyOB=naj_prawyOB,naj_spd=naj_spd, pom=pom, ata=ata, naj_sp=naj_sp, naj_spo=naj_spo, naj_pp=naj_pp, naj_lp=naj_lp,naj_ls=naj_ls, naj_ps=naj_ps)

# logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    form=Login()
    if form.validate_on_submit():
         user=Uzytkownicy.query.filter_by(email=form.email.data).first()
         if user:
              if check_password_hash(user.haslo, form.haslo.data):
                   login_user(user)
                   return redirect(url_for('admin'))

    return render_template('login.html', form=form)

# wyloguj
@app.route('/wyloguj', methods=['GET', 'POST'])
@login_required
def wyloguj():
     logout_user()
     return redirect(url_for('login'))
     

# dodawanie klubu
@app.route('/klub', methods=['GET', 'POST'])
@login_required
def klub():
     klub_obecny = current_user.druzyny.id if current_user.druzyny else None
     zawodnicy = pobierz_zawodnikow(klub_obecny)
     form = TeamForm()
     addp = AddPlayerForm()

     if form.validate_on_submit():
        nazwa = form.nazwa.data

        takisam_team = Druzyny.query.filter_by(nazwa=nazwa).first()
        if takisam_team is not None:
            flash('Nazwa drużyny jest już zajęta. Proszę wybrać inną nazwę.')
            return redirect(url_for('admin'))

        if current_user.druzyny is not None:
            flash('Możesz posiadać tylko jedną drużynę.')
            return redirect(url_for('admin'))

        druzyna = Druzyny(nazwa=nazwa, uzytkownik=current_user)
        db.session.add(druzyna)
        db.session.commit()
        flash('Drużyna została utworzona.')
        return redirect(url_for('admin'))

     return render_template('klub.html',zawodnicy=zawodnicy, form=form, addp=addp)

# Dodawanie zawodnika
@app.route('/addplayer', methods=['GET', 'POST'])
@login_required
def addplayer():
    addp = AddPlayerForm()
    form = TeamForm()
    if addp.validate_on_submit():
        player = Player(
            imie=addp.imie.data,
            nazwisko=addp.nazwisko.data,
            wzrost=addp.wzrost.data,
            waga=addp.waga.data,
            pozycja=addp.pozycja.data,
            szybkosc=addp.szybkosc.data,
            sila=addp.sila.data,
            drybling=addp.drybling.data,
            strzal=addp.strzal.data,
            defensywa=addp.defensywa.data,
            podania=addp.podania.data,
            noga=addp.noga.data,
            druzyna_id=current_user.druzyny.id 
        )
        db.session.add(player)
        db.session.commit()
        return redirect(url_for('klub'))

    return render_template('klub.html', addp=addp, form=form)


# rejestracja
@app.route('/rejestracja', methods=['GET', 'POST'])
def rejestracja():
    form = RejestracjaForm()

    if form.validate_on_submit():
        haslo_hash = generate_password_hash(form.haslo.data)
        uzytkownik = Uzytkownicy(
            imie=form.imie.data,
            nazwisko=form.nazwisko.data,
            email=form.email.data,
            haslo=haslo_hash,
        )
        db.session.add(uzytkownik)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('rejestracja.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)