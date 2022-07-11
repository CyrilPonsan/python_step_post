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
    # tri de la liste des courriers non distribués par ordre décroissant
    # list_statuts.sort(key=lambda x: x["date"], reverse=True)
    return list_statuts


async def read_all_courriers(db: Session, token: str, filter: bool):
    user_id = await read_current_user_id(db, token)
    list_courriers = crud.read_all_courriers(db, user_id)
    filtered_list = []
    x = 5 if filter else 7
    for courrier in list_courriers:
        if courrier.statutcourriers[-1].statut_id < x:
            filtered_list.append(courrier)
    # affichage du total des courriers non distribués
    print(f"{len(list_courriers)} courriers.")
    return await create_list_courriers(filtered_list)


async def read_current_user_id(db: Session, token: str):
    current_user = await service_user.get_current_user(token)
    return crud.get_user_by_email(db, current_user.username).id
