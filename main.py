from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, Base, get_db
from .logica import encolar_mision, desencolar_mision, reconstruir_cola

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/personajes")
def crear_personaje(personaje: schemas.PersonajeCreate, db: Session = Depends(get_db)):
    db_personaje = models.Personaje(nombre=personaje.nombre)
    db.add(db_personaje)
    db.commit()
    db.refresh(db_personaje)
    return db_personaje

@app.post("/misiones")
def crear_mision(mision: schemas.MisionCreate, db: Session = Depends(get_db)):
    db_mision = models.Mision(**mision.dict())
    db.add(db_mision)
    db.commit()
    db.refresh(db_mision)
    return db_mision

@app.post("/personajes/{id}/misiones/{mision_id}")
def aceptar_mision(id: int, mision_id: int, db: Session = Depends(get_db)):
    return encolar_mision(db, id, mision_id)

@app.post("/personajes/{id}/completar")
def completar_mision(id: int, db: Session = Depends(get_db)):
    mision_id = desencolar_mision(db, id)
    if mision_id is None:
        raise HTTPException(status_code=404, detail="No hay misiones para completar")

    mision = db.query(models.Mision).get(mision_id)
    personaje = db.query(models.Personaje).get(id)
    personaje.experiencia += mision.experiencia
    db.commit()
    return {"mensaje": f"Misión '{mision.titulo}' completada", "xp_ganada": mision.experiencia}

@app.get("/personajes/{id}/misiones")
def listar_misiones(id: int, db: Session = Depends(get_db)):
    cola = reconstruir_cola(id, db)
    misiones = []
    for mision_id in cola.to_list():
        mision = db.query(models.Mision).get(mision_id)
        misiones.append(mision)
    return misiones