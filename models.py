from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    experiencia = Column(Integer, default=0)
    misiones = relationship("PersonajeMision", back_populates="personaje")

class Mision(Base):
    __tablename__ = "misiones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descripcion = Column(String)
    experiencia = Column(Integer)
    personajes = relationship("PersonajeMision", back_populates="mision")

class PersonajeMision(Base):
    __tablename__ = "personaje_mision"

    id = Column(Integer, primary_key=True, index=True)
    personaje_id = Column(Integer, ForeignKey("personajes.id"))
    mision_id = Column(Integer, ForeignKey("misiones.id"))

    personaje = relationship("Personaje", back_populates="misiones")
    mision = relationship("Mision", back_populates="personajes")
