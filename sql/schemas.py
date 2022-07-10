from pydantic import BaseModel
from datetime import datetime


class CourrierBase(BaseModel):
    type: int
    bordereau: int
    nom: str
    prenom: str
    civilite: str
    adresse: str
    complement: str
    code_postal: str
    ville: str
    telephone: str


class CourrierCreate(CourrierBase):
    pass


class Courrier(CourrierBase):
    id: int
    expediteur_id: int

    class Config:
        orm_mode = True


class EnvoiEnCours(BaseModel):
    courrier: Courrier
    date: datetime
    statut: int


class StatutBase(BaseModel):
    etat: str


class StatutCreate(StatutBase):
    pass


class Statut(StatutBase):
    id: int

    class Config:
        orm_mode = True


class StatutCourrierBase(BaseModel):
    facteur_id: int
    date: datetime


class StatutCourrierCreate(StatutCourrierBase):
    pass


class StatutCourrier(StatutCourrierBase):
    id: int
    courrier_id: int
    statut_id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
