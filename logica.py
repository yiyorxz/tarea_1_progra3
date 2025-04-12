from sqlalchemy.orm import Session
from models import Personaje, Mision, PersonajeMision
from cola import Cola

def aceptar_mision(db: Session, personaje_id: int, mision_id: int):
    personaje = db.query(Personaje).get(personaje_id)
    cola = Cola()

    # Cargar misiones actuales
    misiones_actuales = (
        db.query(PersonajeMision)
        .filter_by(personaje_id=personaje_id)
        .order_by(PersonajeMision.orden)
        .all()
    )
    for pm in misiones_actuales:
        cola.enqueue(pm)

    nuevo_orden = cola.size() + 1
    nueva_mision = PersonajeMision(personaje_id=personaje_id, mision_id=mision_id, orden=nuevo_orden)
    db.add(nueva_mision)
    db.commit()


def completar_mision(db: Session, personaje_id: int):
    misiones = (
        db.query(PersonajeMision)
        .filter_by(personaje_id=personaje_id)
        .order_by(PersonajeMision.orden)
        .all()
    )
    if not misiones:
        return None

    primera = misiones[0]
    personaje = db.query(Personaje).get(personaje_id)
    mision = db.query(Mision).get(primera.mision_id)

    personaje.xp += mision.xp
    db.delete(primera)
    db.commit()
    return mision


def obtener_misiones(db: Session, personaje_id: int):
    misiones = (
        db.query(PersonajeMision)
        .filter_by(personaje_id=personaje_id)
        .order_by(PersonajeMision.orden)
        .all()
    )
    return [db.query(Mision).get(pm.mision_id) for pm in misiones]
