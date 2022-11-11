from app.database.database import Base
from sqlalchemy import (Integer, String,Boolean,DateTime,
                ForeignKey, Column, UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType
from uuid import uuid4


class Comercio(Base):
    __tablename__ = "comercio"
    id = Column(Integer, primary_key = True,autoincrement=True)
    uuid = Column(UUIDType(binary=False),default=uuid4())
    nombre = Column(String(100))
    activo = Column(Boolean,default=True)
    email_contacto = Column(String(50),nullable=True)
    telefono_contacto = Column(String(15))
    api_key = Column(UUIDType(binary=False),default=uuid4())
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    empleados = relationship("Empleado", back_populates="comercio",lazy='dynamic')


class Empleado(Base):
    __tablename__ = "empleado"
    
    id = Column(Integer, primary_key = True,autoincrement=True)
    uuid = Column(UUIDType(binary=False),default=uuid4())
    nombre = Column(String(40))
    apellidos = Column(String(40))
    pin = Column(String(6))
    comercio_id = Column(Integer, ForeignKey("comercio.id"))
    comercio = relationship("Comercio", back_populates="empleados")
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    activo =  Column(Boolean,default=True)



