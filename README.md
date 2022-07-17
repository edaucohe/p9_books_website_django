# Project 9 - Books website django

## Contents
- [Description](#description)
- [Installation](#installation)
- [Setup](#setup)
- [Use](#use)
- [Helpful links](#links)

## Description <a class="anchor" id="description"></a>

"Project 9 - Books website django" est un programme à réaliser dans le cadre de la formation diplômante d'OpenClassrooms "Développeur d'application Python".

Ce projet a comme but de mettre en place une application web permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

L'application permet de :
- Demander des critiques de livres en créant un ticket.
- Publier des critiques de livres.

Un utilisateur devra pouvoir :
- Se connecter et s'inscrire au site.
- Consulter un flux contenant les derniers billets et critiques.
- Créer des billets afin de demander une critique.
- Créer des critiques en réponse à des billets.
- Pouvoir modifier et supprimer ses propres tickets et critiques.
- S'abonner et se désabonner à d'autres utilisateurs.
- Visualiser les propres abonnements et abonnés.

Quelques consignes à suivre sont :
- Afficher les posts par ordre chronologique, depuis le plus récent au plus ancien.
- Permettre juste une critique par billet.
- Avoir comme option l'enregistrement d'une image par billet crée. 
- L'application web doit être un produit minimum viable (MVP) 

Concernant le côté technique, il faut :
- Mettre en place le framework Django.
- Utiliser SQLite comme base de données.
- Lancer l'application dans le serveur local.

## Installation <a class="anchor" id="installation"></a>

Python version : 3.9

Pour récupérer le projet, lancez :
```
git clone https://github.com/edaucohe/p9_books_website_django.git
```

Pour installer les dépendances du fichier `requirements.txt`, lancez :
```
pip install -r requirements.txt
```

Pour créer l'environnement virtuel, placez-vous dans le dossier `../projet9` et tapez :
```
python -m venv env  
```

Pour activer l'environnement virtuel, tapez :

- Sur windows
```
source env/Scripts/activate
```
- Sur Mac/Linux
```
source env/bin/activate
```

## Setup <a class="anchor" id="setup"></a>

Rien à signaler.

## Use <a class="anchor" id="use"></a>

Pour récupérer la base de données préalablement remplie, placez-vous dans le dossier `../projet9/merchex` et lancez :
```
python manage.py migrate  
```
Pour démarrer l'application, lancez :
```
python manage.py runserver  
```

Une fois le serveur local lancé, adressez-vous au lien du serveur local (voir [Helpful links](#links)) pour commencer à utiliser l'application.

Vous pouvez créer un nouvel utilisateur grâce au formulaire d'inscription. Néanmoins, la base de données est déjà remplie 
avec des utilisateurs fictifs. Vous trouverez ci-listée les coordonnées de ces utilisateurs fictifs :

| Nom d'utilisateur | Mot de passe |
|:-----------------:|:------------:|
|       anne        |    hianne    |
|       tony        |    hitony    |
|       john        |    hijohn    |
|       mari        |    himari    |

Vous pouvez aussi accéder au site d'administration en tant qu'administrateur,
il faut juste s'adresser au http://127.0.0.1:8000/admin/ et tapez les coordonnées ci-listées :

| Nom d'utilisateur | Mot de passe |
|:-----------------:|:------------:|
|       admin       |   hiadmin    |

Dans ce site, vous aurez l'affichage des objects sauvegardés dans la base de données.

Finalement, et afin d'arrêter le serveur local, tapez *ctrl + c* dans le terminal. 

## Helpful links <a class="anchor" id="links"></a>

Lien du serveur local par default : http://127.0.0.1:8000/
