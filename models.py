from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    experiencia = Column(Integer, default=0)

    misiones = relationship("PersonajeMision", backref="personaje")

class Mision(Base):
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descripcion = Column(String)
    experiencia = Column(Integer)

    personajes = relationship("PersonajeMision", backref="mision")

class PersonajeMision(Base):
    __tablename__ = "personaje_mision"

    id = Column(Integer, primary_key=True, index=True)
    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    mision_id = Column(Integer, ForeignKey("misiones.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
