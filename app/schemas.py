from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Union


class ComercioBase(BaseModel):
    nombre: str
    email_contacto: EmailStr | None = None
    telefono_contacto: str | None = None

    class Config:
        orm_mode = True

class EmpleadoBase(BaseModel):
    nombre: str
    apellidos: str
    pin: str
   

    class Config:
        orm_mode = True




