from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Personaje, Mision, PersonajeMision
from schemas import PersonajeCreate, MisionCreate
from datetime import datetime

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.post("/personajes")
def crear_personaje(personaje: PersonajeCreate, db: Session = Depends(get_db)):
    nuevo = Personaje(nombre=personaje.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.post("/misiones")
def crear_mision(mision: MisionCreate, db: Session = Depends(get_db)):
    nueva = Mision(**mision.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    existe = db.query(PersonajeMision).filter_by(personaje_id=personaje_id, mision_id=mision_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="Misión ya aceptada.")
    pm = PersonajeMision(personaje_id=personaje_id, mision_id=mision_id, timestamp=datetime.utcnow())
    db.add(pm)
    db.commit()
    return {"mensaje": "Misión aceptada."}

@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    pm = db.query(PersonajeMision).filter_by(personaje_id=personaje_id).order_by(PersonajeMision.timestamp.asc()).first()
    if not pm:
        raise HTTPException(status_code=404, detail="No hay misiones para completar.")
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()
    mision = db.query(Mision).filter_by(id=pm.mision_id).first()
    personaje.experiencia += mision.experiencia
    db.delete(pm)
    db.commit()
    return {"mensaje": f"Misión '{mision.titulo}' completada. XP ganada: {mision.experiencia}"}

@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int, db: Session = Depends(get_db)):
    pm = db.query(PersonajeMision).filter_by(personaje_id=personaje_id).order_by(PersonajeMision.timestamp.asc()).all()
    misiones = []
    for relacion in pm:
        mision = db.query(Mision).filter_by(id=relacion.mision_id).first()
        misiones.append({
            "id": mision.id,
            "titulo": mision.titulo,
            "descripcion": mision.descripcion
        })
    return misiones
@app.get("/")
def root():
    return {"mensaje": "Bienvenido al sistema de misiones RPG"}
