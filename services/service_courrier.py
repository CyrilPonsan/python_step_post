from fastapi import HTTPException
from sqlalchemy.orm import Session

from services import service_user
from sql import crud, models


async def create_list_courriers(list_courriers: list[models.Courrier]):
    list_statuts = []
    for courrier in list_courriers:
        list_statuts.append({
            "courrier": courrier,
            "statut": courrier.statutcourriers[-1].statut_id,
            "date": courrier.statutcourriers[-1].date
        })
    # total des courriers transformés et retournés au front-end
    print(f"{len(list_statuts)} courriers traîtés")
    return list_statuts


def filter_courriers(liste: list[models.Courrier], filter: bool):
    filtered_list = []
    for courrier in liste:
        if filter:
            if courrier.statutcourriers[-1].statut_id < 5:
                filtered_list.append(courrier)
        else:
            if courrier.statutcourriers[-1].statut_id > 4:
                filtered_list.append(courrier)
    return filtered_list


async def read_all_courriers(db: Session, token: str, filter: bool):
    user_id = await read_current_user_id(db, token)
    list_courriers = crud.read_all_courriers(db, user_id)
    # affichage du total des courriers enregistrés dans la bdd
    print(f"{len(list_courriers)} courriers trouvés dans la bdd.")
    return await create_list_courriers(filter_courriers(list_courriers, filter))


async def read_bordereau(db: Session, bordereau: str):
    bordereau = test_bordereau(bordereau)
    courrier = crud.read_bordereau(db, bordereau)
    if not courrier:
        raise HTTPException(status_code=404, detail="courrier not found")
    return {"courrier": courrier, "statuts": courrier.statutcourriers}


async def read_courriers_by_name(db: Session, nom: str, str_filter: str):
    list_courriers = crud.read_courriers_by_nom(db, nom)
    if not list_courriers:
        raise HTTPException(status_code=404, detail="destinataire not found")
    filtered_list = filter_courriers(list_courriers, test_filter(str_filter))
    return await create_list_courriers(filtered_list)


async def read_current_user_id(db: Session, token: str):
    current_user = await service_user.get_current_user(token)
    return crud.get_user_by_email(db, current_user.username).id


def test_bordereau(bordereau):
    try:
        return int(bordereau)
    except:
        raise HTTPException(status_code=422, detail="dans le cul lulu")


def test_filter(str_filter):
    return str_filter == "True"
