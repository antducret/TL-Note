# TL Projet
## A. Introduction
Ce projet a pour but de récupérer les informations contenues dans une liste de cartes agents journalières d'un conducteur TL, afin de créer une liste de note intuitive sur le système simplenote.


## B. Processus

### B.1. Reception données sous forme pdf

Sous forme de dossier dans lequel placé les pdfs à traiter

### B.2. Extraction des informations de chaque pdf sous forme de datapack

- Date
- Type de journée
- n° TOUR
- listevoiture
- horairesdétaillés

### B.3. Déplacement/Suppresion des fichiers traités

A décider avec client...

### B.4. Creation d'une note publiable sur simplenote sous forme de string


- #### Titre (visible dans la liste SIMPLENOTE)
    "MONTH-DAY DAYLETTER LOGOS STARTHOUR STARTPLACE"

    - Logos : liste de symboles correspondant à certains détails du tour. Voir liste des correspondances logos : "Logos"

    NOMCODE | LOGO | Description

    Format CSV ? --> Modifiable dacilement par le client ?

- #### Détails tour

    - n°tour DAY/MONTH/ANNEE
    -
    - n° voiture 1
    - Tour voiture 1 : Heure0? LieuPrise Heure1? Heure2? LieuDepot
    - n° voiture n
    - Tour voiture n : Heure0? LieuPrise Heure1? Heure2? LieuDepot
    -
    - horaires détaillés

### B.5. Publication de la note
- more information on SIMPLENOTE : https://kendersec.github.io/SimpleNote/SimpleNote-API-v2.1.3.pdf

- Remplacement des notes de même date ?

### B.6. Suppression des notes périmées
