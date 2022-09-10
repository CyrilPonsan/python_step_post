from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# username est le nom donné au champ email dans la bdd
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.username == email).first()


def read_courriers(db: Session, user_id: int):
    sc = models.StatutCourrier
    co = models.Courrier
    return db.query(co.id, co.type, co.bordereau, co.civilite, co.prenom, co.nom, func.max(sc.statut_id).label("etat"),
                    func.max(sc.date).label("date")) \
        .select_from(sc) \
        .filter(sc.courrier_id == co.id, co.expediteur_id == user_id) \
        .group_by(sc.courrier_id)\
        .having(func.max(sc.statut_id) < 5) \
        .order_by(sc.date.desc()) \
        .all()


def read_historique(db: Session, user_id: int):
    sc = models.StatutCourrier
    co = models.Courrier
    return db.query(co.id, co.type, co.bordereau, co.civilite, co.prenom, co.nom, func.max(sc.statut_id).label("etat"),
                    func.max(sc.date).label("date")) \
        .select_from(sc) \
        .filter(sc.courrier_id == co.id, co.expediteur_id == user_id) \
        .group_by(sc.courrier_id) \
        .having(func.max(sc.statut_id) > 4) \
        .order_by(sc.date.desc()) \
        .all()


def read_last_statut(db: Session, courrier_id: int):
    return db.query(models.StatutCourrier.statut_id) \
        .order_by(models.StatutCourrier.date.desc()) \
        .join(models.Courrier) \
        .filter(models.Courrier.id == courrier_id).first()


# récupération d'un courrier par son numéro de bordereau
def read_bordereau(db: Session, bordereau: int, user_id: int):
    return db.query(models.Courrier) \
        .filter(models.Courrier.expediteur_id == user_id, models.Courrier.bordereau == bordereau) \
        .first()


# récupération des courriers envoyés à un destinataire précis
def read_courriers_by_nom(db: Session, nom: str):
    return db.query(models.Courrier).filter(models.Courrier.nom == nom).all()


def testStatut(value: int):
    if 4 < value < 6:
        return True
