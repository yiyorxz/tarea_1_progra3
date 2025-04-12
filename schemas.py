from pydantic import BaseModel

class PersonajeCreate(BaseModel):
    nombre: str

class MisionCreate(BaseModel):
    titulo: str
    descripcion: str
    experiencia: int
