from .cola import Cola
from .models import PersonajeMision
from sqlalchemy.orm import Session

def reconstruir_cola(personaje_id: int, db: Session):
    cola = Cola()
    relaciones = db.query(PersonajeMision).filter_by(personaje_id=personaje_id).order_by(PersonajeMision.id).all()
    for rel in relaciones:
        cola.enqueue(rel.mision_id)
    return cola

def encolar_mision(db: Session, personaje_id: int, mision_id: int):
    nueva_rel = PersonajeMision(personaje_id=personaje_id, mision_id=mision_id)
    db.add(nueva_rel)
    db.commit()
    db.refresh(nueva_rel)
    return nueva_rel

def desencolar_mision(db: Session, personaje_id: int):
    cola = reconstruir_cola(personaje_id, db)
    mision_id = cola.dequeue()
    if mision_id is None:
        return None

    relacion = db.query(PersonajeMision).filter_by(personaje_id=personaje_id, mision_id=mision_id).first()
    if relacion:
        db.delete(relacion)
        db.commit()
    return mision_id