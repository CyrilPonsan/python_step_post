from datetime import datetime, timedelta
import mysql.connector
import mariadb
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sql import models

mydb = mariadb.connect(
    host="j5zntocs2dn6c3fj.chr7pe7iynqr.eu-west-1.rds.amazonaws.com",
    user="htpkkl1ks2cterll",
    password="d60ca1mc7jx8aepu",
    database="bfph5v8vakot3nhn"
)
destinataires = {
    "user_id": 1,
    "civilite": "mr",
    "prenom": "jacques",
    "nom": "durand",
    "adresse": "23 rue Xavier Pinson",
    "code_postal": "64000",
    "ville": "pau",
}, {
    "user_id": 1,
    "civilite": "mr",
    "prenom": "xavier",
    "nom": "pinson",
    "adresse": "12 rue kevin troisquarts",
    "code_postal": "64666",
    "ville": "gelos",
}, {
    "user_id": 1,
    "civilite": "",
    "prenom": "service presse",
    "nom": "mairie",
    "adresse": "2 place royale",
    "code_postal": "6000",
    "ville": "pau",
}, {
    "user_id": 1,
    "civilite": "",
    "prenom": "service comm",
    "nom": "mairie",
    "adresse": "2 place royale",
    "code_postal": "64000",
    "ville": "pau",
}, {
    "user_id": 1,
    "civilite": "mme",
    "prenom": "gilberte",
    "nom": "dupontelle",
    "adresse": "56 rue xavier pinson",
    "code_postal": "64666",
    "ville": "gelos",
}, {
    "user_id": 1,
    "civilite": "mme",
    "prenom": "bérangère",
    "nom": "de la roche-foucault",
    "adresse": "34 rue léo poivrier",
    "code_postal": "64230",
    "ville": "bizanos",
}, {
    "user_id": 1,
    "civilite": "mr",
    "prenom": "rené",
    "nom": "dupont",
    "adresse": "48 place verdun",
    "code_postal": "64000",
    "ville": "pau",
}, {
    "user_id": 1,
    "civilite": "mr",
    "prenom": "albert",
    "nom": "dupontel",
    "adresse": "296 bvd Olga Ducresne",
    "code_postal": "64470",
    "ville": "serres-castet",
},
etats = [
    "en attente",
    "pris en charge",
    "avisé",
    "mis en instance",
    "distribué",
    "npai",
    "retourné à l'expéditeur"
]

def create_fixtures(db: Session):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("Abcd@1234")
    db_user = models.User(username="toto@toto.fr", password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_etat: models.Statut
    for etat in etats:
        db_etat = models.Statut(etat=etat)
        db.add(db_etat)
        db.commit()
        db.refresh(db_etat)
    bordereau = 10000
    db_courrier: models.Courrier
    for dest in destinataires:
        for i in range(20):
            db_courrier = models.Courrier(
                expediteur_id=1,
                type=1,
                bordereau=bordereau,
                civilite=dest["civilite"],
                prenom=dest["prenom"],
                nom=dest["nom"],
                adresse=dest["adresse"],
                complement="",
                code_postal=dest["code_postal"],
                ville=dest["ville"],
                telephone=""
            )
            db.add(db_courrier)
            bordereau += 1
    db.commit()
    db.refresh(db_courrier)
    liste_courriers = db.query(models.Courrier).all()
    x = 0
    db_statut: models.StatutCourrier
    for courrier in liste_courriers:
        if not courrier.statutcourriers:
            for i in range(4):
                db_statut = models.StatutCourrier(
                    facteur_id=1,
                    courrier_id=courrier.id,
                    statut_id=i + 1,
                    date=datetime.now() + timedelta(days=x)
                )
                x += 1
                db.add(db_statut)
    db.commit()
    db.refresh(db_statut)
    db_courrier: models.Courrier
    for dest in destinataires:
        for i in range(500):
            db_courrier = models.Courrier(
                expediteur_id=1,
                type=1,
                bordereau=bordereau,
                civilite=dest["civilite"],
                prenom=dest["prenom"],
                nom=dest["nom"],
                adresse=dest["adresse"],
                complement="",
                code_postal=dest["code_postal"],
                ville=dest["ville"],
                telephone=""
            )
            db.add(db_courrier)
            bordereau += 1
    db.commit()
    db.refresh(db_courrier)
    liste_courriers = db.query(models.Courrier).all()
    x = 0
    db_statut: models.StatutCourrier
    for courrier in liste_courriers:
        if not courrier.statutcourriers:
            for i in range(5):
                db_statut = models.StatutCourrier(
                    facteur_id=1,
                    courrier_id=courrier.id,
                    statut_id=i + 1,
                    date=datetime.now() + timedelta(days=x)
                )
                x += 1
                db.add(db_statut)
    db.commit()
    db.refresh(db_statut)
    return True
