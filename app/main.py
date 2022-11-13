from sqlite3 import IntegrityError
from app.database.database import Base
from fastapi import Depends, FastAPI, HTTPException, status
from app.authentication import get_current_username
from app.models import Comercio, Empleado
from app.database import database
from app.schemas import ComercioBase, EmpleadoBase
from app.exceptions import (DuplicatedPinError,
                            InvalidEmpleadoError, NoEmpleadoError)

app = FastAPI()

Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/comercio', status_code=status.HTTP_201_CREATED)
def create_comercio(comercio: ComercioBase, db: database.SessionLocal = Depends(get_db)):
    new_comercio = Comercio(nombre=comercio.nombre)
    db.add(new_comercio)
    db.commit()
    db.refresh(new_comercio)
    return new_comercio


@app.get('/empleados', status_code=status.HTTP_200_OK)
def get_empleados(uuid_empleado: str | None = None, request=Depends(get_current_username)):
    comercio = request[0]
    if uuid_empleado:
        empleado = comercio.empleados.filter(
            Empleado.uuid == uuid_empleado).first()
        if not empleado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API KEY no Exist",
            )
        return empleado
    else:
        empleados = comercio.empleados.all()
        return empleados


@app.post('/empleados', status_code=status.HTTP_201_CREATED)
def post_empleados(empleado: EmpleadoBase, db: database.SessionLocal = Depends(get_db),
                   request=Depends(get_current_username)):

    comercio = request[0]
    new_empleado = Empleado(
        nombre=empleado.nombre,
        apellidos=empleado.apellidos,
        pin=empleado.pin,
        comercio_id=comercio.id
    )
    try:
        db.add(new_empleado)
        db.commit()
        db.refresh(new_empleado)
    except IntegrityError:
        raise HTTPException(
            DuplicatedPinError(),
            detail="Internal Server Integrity")

    return new_empleado


@app.put('/empleados', status_code=status.HTTP_201_CREATED)
def put_empleados(empleado: EmpleadoBase, db: database.SessionLocal = Depends(get_db),
                  request=Depends(get_current_username), uuid_empleado: str | None = None,):
    comercio = request[0]
    if not uuid_empleado:
        raise HTTPException(
            status_code=404,
            detail="Key no valid")

    emp = comercio.empleados.filter(Empleado.uuid == uuid_empleado).first()
    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Do not exist employee")
    emp.nombre = empleado.nombre
    emp.apelldios = empleado.apellidos
    emp.pin = empleado.pin
    db.merge(emp)
    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            DuplicatedPinError(),
            detail="Do not exist employee")

    return emp


@app.delete('/empleados', status_code=status.HTTP_200_OK)
def delete_empleados(db: database.SessionLocal = Depends(get_db),
                     request=Depends(get_current_username), uuid_empleado: str | None = None):
    comercio = request[0]
    if not uuid_empleado:
        raise HTTPException(
            status_code=404,
            detail="Key not valid")

    emp = comercio.empleados.filter(Empleado.uuid == uuid_empleado).first()
    if not emp:
        raise HTTPException(
            status_code=404,
            detail="Do not exist employee")
    emp_delete = db.merge(emp)
    db.delete(emp_delete)
    db.commit()
    return "Done"
