from sqlalchemy.orm import Session

from services import service_user
from sql import crud


async def read_all_courriers(db: Session, token: str):
    user_id = await read_current_user_id(db, token)
    return await create_list_envois_en_cours(db, user_id)


async def read_current_user_id(db: Session, token: str):
    current_user = await service_user.get_current_user(token)
    return crud.get_user_by_email(db, current_user.username).id


async def create_list_envois_en_cours(db: Session, user_id: int):
    list_courriers = crud.read_all_envois_en_cours(db, user_id)
    list_statuts = []
    for courrier in list_courriers:
        list_statuts.append({
            "courrier": courrier,
            "statut": courrier.statutcourriers[-1].statut_id,
            "date": courrier.statutcourriers[-1].date
        })
    # affichage du total des courriers non distribués
    print(f"{len(list_statuts)} courriers.")
    # tri de la liste des courriers non distribués par ordre décroissant
    list_statuts.sort(key=lambda x: x["date"], reverse=True)
    return list_statuts
