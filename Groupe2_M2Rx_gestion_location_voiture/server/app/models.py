from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import g, url_for

from app import db
from config import Config

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64))
    postnom = db.Column(db.String(64))
    prenom = db.Column(db.String(64))
    date_naissance = db.Column(db.DateTime)
    email = db.Column(db.String(64))
    adresse = db.Column(db.String(128))
    nationalite = db.Column(db.String(64))
    telephone = db.Column(db.String(64))

    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    locations = db.relationship('Location', backref='clt')

    def to_json(self):
        return {
            'id': self.id,
            'uri': url_for('get_id_client', id_client=self.id, _external=True),
            'username': self.username,
            'password': self.password_hash,
            'nom': self.nom,
            'postnom': self.postnom,
            'prenom': self.prenom,
            'date_naissance': self.date_naissance,
            'email': self.email,
            'adresse': self.adresse,
            'nationalite': self.nationalite,
            'telephone': self.telephone
        }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # Si le token est valide mais qu'il a expiré
        except BadSignature:
            return None # Si le token est invalide
        return Client.query.get(data['id'])


class Voiture(db.Model):
    __tablename__ = 'voitures'
    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(32))
    immatriculation = db.Column(db.String(32), index=True, unique=True)
    categorie = db.Column(db.String(32))
    modele = db.Column(db.String(32))
    disponible = db.Column(db.Boolean)
    kilometrage = db.Column(db.Integer)
    type_voiture = db.Column(db.String(32))
    couleur = db.Column(db.String(32))
    locations = db.relationship('Location', backref='voiture')

    def to_json(self):
        return {
            'id': self.id,
            'uri': url_for('get_id_voiture', id_voiture=self.id, _external=True),
            'marque': self.marque,
            'immatriculation': self.immatriculation,
            'categorie': self.categorie,
            'modele': self.modele,
            'disponible': self.disponible,
            'kilometrage': self.kilometrage,
            'type_voiture': self.type_voiture,
            'couleur': self.couleur,
        }



class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    date_location = db.Column(db.DateTime)
    id_voiture = db.Column(db.Integer, db.ForeignKey('voitures.id'))
    id_client = db.Column(db.Integer, db.ForeignKey('clients.id'))

    def to_json(self):
        username = ""
        if self.clt is not None:
            username = self.clt.username

        return {
            'id': self.id,
            'uri': url_for('get_location_id', location_id=self.id, _external=True),
            'date_location': self.date_location,
            'voiture_prop': self.voiture.marque + ' ' + self.voiture.modele + ' : ' + self.voiture.immatriculation,
            'username': username,
            'id_voiture': self.id_voiture,
            'id_client': self.id_client
        }
    
