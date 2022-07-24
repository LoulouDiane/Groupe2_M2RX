from flask import Flask, jsonify, abort, make_response, request, url_for, g
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app, db
from app.models import Client, Voiture, Location

LONG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
SHORT_DATE_FORMAT = '%Y-%m-%d'


auth = HTTPBasicAuth()

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403) #We have changed 401 error code to 403 to prevent web browser to launch the ugly login form

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    client = Client.verify_auth_token(username_or_token)
    if not client:
        # try to authenticate with username/password
        client = Client.query.filter_by(username=username_or_token).first()
        if not client or not client.verify_password(password):
            return False
    g.client = client
    return True


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.client.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

################################# clients #################################

@app.route('/api/clients', methods=['GET'])
@auth.login_required
def get_clients():
    clients = Client.query.all()
    return jsonify([client.to_json() for client in clients])

@app.route('/api/clients/<int:id_client>', methods=['GET'])
@auth.login_required
def get_id_client(id_client):
    client = Client.query.filter_by(id=id_client).first()
    if client is None:
        abort(404)
    return jsonify({'client': client.to_json()})


@app.route('/api/clients', methods=['POST'])
def new_client():
    username = request.json.get('username')
    password = request.json.get('password')
    nom = request.json.get('nom')
    postnom = request.json.get('postnom')
    prenom = request.json.get('prenom')
    date_naissance = datetime.strptime(request.json['date_naissance'], SHORT_DATE_FORMAT)
    email = request.json.get('email')
    adresse = request.json.get('adresse')
    nationalite = request.json.get('nationalite')
    telephone = request.json.get('telephone')

    if username is None or password is None  or nom is None or prenom is None or date_naissance is None \
            or email is None or adresse is None or nationalite is None or telephone is None :
        print("missing crucial informations")
        abort(400) # missing crucial informations
    if Client.query.filter_by(username = username).first() is not None:
        print("username already existing")
        abort(400) # username already existing
    client = Client(username=username, nom=nom, postnom=postnom, prenom=prenom, date_naissance=date_naissance,
                  email=email, adresse=adresse, nationalite=nationalite, telephone=telephone)
    client.hash_password(password)
    db.session.add(client)
    db.session.commit()
    return jsonify({'username': client.username}), 201, {'uri': url_for('get_id_client', id_client=client.id, _external=True)}

@app.route('/api/clients/<int:id_client>', methods=['PUT'])
@auth.login_required
def update_client(id_client):
    client = Client.query.filter_by(id=id_client).first()
    if client is None:
        abort(404)
    if not request.json:
        print("bad request")
        abort(400)

    client.username = request.json.get('username', client.username)
    client.nom = request.json.get('nom', client.nom)
    client.postnom = request.json.get('postnom', client.postnom)
    client.prenom = request.json.get('prenom', client.prenom)
    client.date_naissance = datetime.strptime(request.json['date_naissance'], SHORT_DATE_FORMAT)
    client.email = request.json.get('email', client.email)
    client.adresse = request.json.get('adresse', client.adresse)
    client.nationalite = request.json.get('nationalite', client.nationalite)
    client.telephone = request.json.get('telephone', client.telephone)

    password = request.json.get('password', client.password_hash)
    if password != client.password_hash:
        client.hash_password(password)

    db.session.add(client)
    db.session.commit()
    return jsonify({'client': client.to_json()})

@app.route('/api/clients/<int:id_client>', methods=['DELETE'])
@auth.login_required
def delete_client(id_client):
    client = Client.query.filter_by(id=id_client).first()
    if client is None:
        abort(404)

    db.session.delete(client)
    db.session.commit()
    return jsonify({'result': True})

################## end clients ############################################


############################ voitures ######################

@app.route('/api/voitures', methods=['GET'])
@auth.login_required
def get_voitures():
    voitures = Voiture.query.all()
    return jsonify({'voitures': [voiture.to_json() for voiture in voitures]})

@app.route('/api/voitures/<int:id_voiture>', methods=['GET'])
@auth.login_required
def get_id_voiture(id_voiture):
    voiture = Voiture.query.filter_by(id=id_voiture).first()
    if voiture is None:
        abort(404)
    return jsonify({'voiture': voiture.to_json()})

@app.route('/api/voitures', methods=['POST'])
@auth.login_required
def create_voiture():
    print("#"*15)
    print(request.json.get('role'))
    print("#" * 15)
    if not request.json or 'immatriculation' not in request.json:
        abort(400) # bad request
    if request.json.get('role').upper() != 'ADMIN':
        print('here ::::', request.json.get('role'))
        abort(403)

    voiture = Voiture(
        categorie=request.json['categorie'],
        marque=request.json['marque'],
        modele=request.json['modele'],
        immatriculation=request.json['immatriculation'],
        disponible=True,
        kilometrage=request.json['kilometrage'],
        type_voiture=request.json['type_voiture'],
        couleur=request.json['couleur']
    )
    db.session.add(voiture)
    db.session.commit()
    return jsonify({'voiture': voiture.to_json()}), 201 # Created

@app.route('/api/voitures/<int:id_voiture>', methods=['PUT'])
@auth.login_required
def update_voiture(id_voiture):
    voiture = Voiture.query.filter_by(id=id_voiture).first()
    if voiture is None:
        abort(404)
    if not request.json:
        abort(400)

    voiture.categorie = request.json.get('categorie', voiture.categorie)
    voiture.modele = request.json.get('modele', voiture.modele)
    voiture.marque = request.json.get('marque', voiture.marque)
    voiture.immatriculation = request.json.get('immatriculation', voiture.immatriculation)

    if request.json.get('disponible'):
        voiture.disponible = True

    voiture.kilometrage = request.json.get('kilometrage', voiture.kilometrage)
    voiture.type_voiture = request.json.get('type_voiture', voiture.type_voiture)
    voiture.couleur = request.json.get('couleur', voiture.couleur)

    db.session.add(voiture)
    db.session.commit()
    return jsonify({'voiture': voiture.to_json()})

@app.route('/api/voitures/<int:id_voiture>', methods=['DELETE'])
@auth.login_required
def delete_voiture(id_voiture):
    voiture = Voiture.query.filter_by(id=id_voiture).first()
    if voiture is None:
        abort(404)
    db.session.delete(voiture)
    db.session.commit()
    return jsonify({'result': True})

################################# end voitures ########################

##################################### location #########################

@app.route('/api/voitures/locations', methods=['GET'])
@auth.login_required
def get_locations():
    locations = Location.query.all()
    return jsonify({'locations': [res.to_json() for res in locations]})

@app.route('/api/voitures/locations/<int:location_id>', methods=['GET'])
@auth.login_required
def get_location_id(location_id):
    res = Location.query.filter_by(id=location_id).first()
    if res is None:
        abort(404)
    return jsonify({'locations': res.to_json()})

@app.route('/api/voitures/locations', methods=['POST'])
@auth.login_required
def create_location():
    r_date = datetime.strptime(request.json['date_location'], LONG_DATE_FORMAT)
    c_id = request.json['id_voiture']
    u_id = Client.query.filter_by(username=request.json['id_client']).first().id

    voiture = Voiture.query.filter_by(id=c_id).first()
    if not voiture.disponible:
        abort(400)
    res = Location(
        date_location = r_date,
        id_voiture = c_id,
        id_client = u_id
    )

    voiture.disponible = False

    db.session.add(res)
    db.session.commit()
    return jsonify({'location': res.to_json()}), 201 # Created

@app.route('/api/voitures/locations/<int:location_id>', methods=['PUT'])
@auth.login_required
def update_location(location_id):
    res = Location.query.filter_by(id=location_id).first()
    if res is None:
        abort(404)
    if not request.json:
        abort(400)

    res.location_date = request.json.get('date_location', res.location_date)
    res.id_client = request.json.get('id_client', res.id_client)
    res.id_voiture = request.json.get('id_voiture', res.id_voiture)
    
    db.session.save(res)
    db.session.commit()
    return jsonify({'locations': res.to_json()})

@app.route('/api/voitures/locations/<int:location_id>', methods=['DELETE'])
@auth.login_required
def delete_location(location_id):
    res = Location.query.filter_by(id=location_id).first()
    if res is None:
        abort(404)
    db.session.delete(res)
    db.session.commit()
    return jsonify({'result': True})

####################### end location ##################""
