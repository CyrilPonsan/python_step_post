from fastapi import HTTPException
from sqlalchemy.orm import Session

from sql import crud, models


# noinspection PyCompatibility
def create_list_courriers(list_courriers: list[models.Courrier]):
    list_statuts = []
    for courrier in list_courriers:
        list_statuts.append({
            "courrier": courrier,
            "statut": courrier.statutcourriers[-1].statut_id,
            "date": courrier.statutcourriers[-1].date
        })
    return list_statuts


def toto(liste: list[models.StatutCourrier]):
    list_toto = []
    for statut in liste:
        list_toto.append({
            "courrier": statut.courrier,
            "statut": statut.statut_id,
            "date": statut.date
        })
    return list_toto


def filter_courriers(liste: list[models.Courrier], filter: bool):
    filtered_list = []
    if filter:
        for courrier in liste:
            if courrier.statutcourriers[-1].statut_id < 5:
                filtered_list.append(courrier)
    else:
        for courrier in liste:
            if courrier.statutcourriers[-1].statut_id > 4:
                filtered_list.append(courrier)
    return filtered_list


def read_all_courriers(db: Session, user_id: int):
    user = crud.get_user_by_id(db, user_id)
    list_courriers = crud.read_all_courriers(db, user.id)
    for x in list_courriers:
        print(x.statut_id)
    print(f"{len(list_courriers)} courriers traités")
    return toto(list_courriers)


async def read_bordereau(db: Session, bordereau: str, user_id: int):
    bordereau = test_bordereau(bordereau)
    courrier = crud.read_bordereau(db, bordereau, user_id)
    if not courrier:
        raise HTTPException(status_code=404, detail="courrier not found")
    return {"courrier": courrier, "statuts": courrier.statutcourriers}


async def read_courriers_by_name(db: Session, nom: str, str_filter: str):
    list_courriers = crud.read_courriers_by_nom(db, nom)
    if not list_courriers:
        raise HTTPException(status_code=404, detail="destinataire not found")
    filtered_list = filter_courriers(list_courriers, test_filter(str_filter))
    return await create_list_courriers(filtered_list)


def test_bordereau(bordereau):
    try:
        return int(bordereau)
    except:
        raise HTTPException(status_code=422, detail="dans le cul lulu")


def test_filter(str_filter):
    return str_filter == "True"
