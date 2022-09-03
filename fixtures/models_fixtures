from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class Courrier(Base):
    __tablename__ = "courrier"
    id = Column(Integer, primary_key=True, index=True)
    expediteur_id = Column(Integer, ForeignKey("user.id"))
    type = Column(Integer)
    bordereau = Column(Integer, index=True)
    civilite = Column(String(10))
    nom = Column(String(255))
    prenom = Column(String(255))
    adresse = Column(String(255))
    complement = Column(String(255))
    code_postal = Column(String(10))
    ville = Column(String(255))
    telephone = Column(String(20))
    expediteur = relationship("User")
    statutcourriers = relationship("StatutCourrier", lazy="select")


class Statut(Base):
    __tablename__ = "statut"
    id = Column(Integer, primary_key=True, index=True)
    etat = Column(String(255))


class StatutCourrier(Base):
    __tablename__ = "statutcourrier"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    facteur_id = Column(Integer)
    courrier_id = Column(Integer, ForeignKey("courrier.id"))
    statut_id = Column(Integer, ForeignKey("statut.id"))


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    courriers = relationship("Courrier", back_populates="expediteur")
