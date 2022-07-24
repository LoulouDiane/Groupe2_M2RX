# GESTION DE LOCATION DE VOITURES

## I. Création de l'environnement virtuel

1. Installation de python3-sqlalchemy pour le mapping objet relationnel
```bash
$ sudo apt install python3-sqlalchemy
```

2. Installation du gestionnaire des versions de python : **pyenv**
3. Installation de python 3.10
```bash
$ pyenv install 3.10.5
```
4. Activation de python 3.10.5
```bash
$ pyenv global 3.10.5 
```
5. Installation de pipenv le nouveau gestionnaire des packages de python
Suivre ce lien : https://manpages.ubuntu.com/manpages/impish/man1/pipenv.1.html
```bash
$ pip install --user pipenv
```
5. Ajouter le chemin du repertoire de base d'utilisateurs dans la variable d'environnement PATH
Le resultat de la commande : 
```bash
$ python -m site  --user-base
```
exemple : /home/nk/.local

Ouvrir ~/.bashrc avec l'editeur nano 
```bash
$ sudo nano ~/.bashrc
```
et ajouter a la fin ce chemin
```bash

export PATH=/home/nk/.local:$PATH
```
6. Création proprementdite de l'environnement virtuel avec dédans **la version 3.10 de python**

```bash
$ pipenv --python 3.10
```
5. Activation de l'environnement virtuel
```bash
$ pipenv shell
```
6. Installation des dépendances
```bash
$ pipenv install -r requirements.txt
$ pip install python-dotenv
```
7. Si la base de données n'existe pas ou si le dossiers des migrations a été supprimer, aller au point **I.1.** avant de revenir au point **6** pour lancer l'API
8. Lancer l'API 
```bash
$ flask run 
```
## II. Initialisation / Mise à jour de la base de données
Pour ce travail nous avons utilisé une base de données embarquée (SQLite).
1. Initialisation du système des migrations
```bash
$ flask db init 
```
2. Création des scripts des migrations 
```bash
$ flask db migrate 
```
3. Exécution des scripts de migrations sur la base de données 
```bash
$ flask db upgrade 
```
## III. Lancement du Serveur (API Restful)
1. Lancer l'API 
```bash
$ flask run 
```
## III. Lancement du Client
Afin de contourner le blocage des requetes Cross Origin, nous avons consultés le lien suivant:
https://stackoverflow.com/questions/65016580/how-do-i-get-around-cross-origin-requests-being-blocked
Suivant les propositions de l'article, nous avons resolus de lancer le client dans son propre serveur web. Nous avons choisit le serveur web PHP, qui est plus leger.
1. Installer  PHP
```bash
$ sudo apt install php7.4-cli
```
2. lancer le serveur web au port 8000
```bash
$ php -S localhost:8000
```
3. Saisir l'adresse dans un navigateur.
