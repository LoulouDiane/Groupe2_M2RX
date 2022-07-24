# GESTION DE LOCATION DE VOITURES

## I. Création de l'environnement virtuel

1. Installation du gestionnaire des versions de python : **pyenv**
2. Installation de pipenv le nouveau gestionnaire des packages de python
3. Création proprementdite de l'environnement virtuel avec dédans **la version 3.10 de python**

```bash
$ pipenv --python 3.10
```
4. Activation de l'environnement virtuel
```bash
$ pipenv shell
```
5. Installation des dépendances
```bash
$ pipenv install -r requirements.txt
```
6. Si la base de données n'existe pas ou si le dossiers des migrations a été supprimer, aller au point **I.1.** avant de revenir au point **6** pour lancer l'API
7. Lancer l'API 
```bash
$ flask run 
```
## II. Initialisation / Mise à jour de la base de données

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
