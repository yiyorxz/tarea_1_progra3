from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
import logica

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    logica.aceptar_mision(db, personaje_id, mision_id)
    return {"mensaje": "Misión aceptada"}

@app.post("/personajes/{personaje_id}/completar")
def completar(personaje_id: int, db: Session = Depends(get_db)):
    mision = logica.completar_mision(db, personaje_id)
    if not mision:
        raise HTTPException(status_code=404, detail="No hay misiones")
    return {"mensaje": f"Misión '{mision.descripcion}' completada", "xp_ganado": mision.xp}

@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int, db: Session = Depends(get_db)):
    misiones = logica.obtener_misiones(db, personaje_id)
    return [m.descripcion for m in misiones]
