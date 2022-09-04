from passlib.context import CryptContext
from sqlalchemy import func, or_, not_
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


# récupération de tous les courriers
def read_courriers(db: Session, user_id: int):
    sc = models.StatutCourrier
    return db.query(sc) \
        .group_by(sc.courrier_id.desc()) \
        .having(func.max(sc.statut_id) < 5) \
        .join(models.Courrier) \
        .order_by(models.Courrier.bordereau.desc()) \
        .filter(models.Courrier.expediteur_id == user_id) \
        .all()


def read_historique(db: Session, user_id: int):
    return db.query(models.StatutCourrier) \
        .group_by(models.StatutCourrier.courrier_id) \
        .filter(models.StatutCourrier.statut_id > 4) \
        .join(models.Courrier) \
        .order_by(models.Courrier.bordereau.desc()) \
        .filter(models.Courrier.expediteur_id == user_id) \
        .all()


def read_last_statut(db: Session, courrier_id: int):
    return db.query(models.StatutCourrier.statut_id)\
        .order_by(models.StatutCourrier.date.desc())\
        .join(models.Courrier)\
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
