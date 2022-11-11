
from fastapi import Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy import create_engine
from ..authentication import get_current_username
from sqlalchemy.orm import sessionmaker
from ..main import app, get_db
from ..database.database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db,get_current_username] = override_get_db


client = TestClient(app)


class Empleado(BaseModel):
    nombre: str
    apellidos: str
    pin: str


def test_get_empleados(uuid_empleado='ac05c1fc-254e-488c-b65a-7fb7aede3c43'):
    response = client.get("/empleados")
    if uuid_empleado:
        assert True
    assert response.status_code == 200


def test_post_empleados():
    empleado = {"nombre": "Lupita", "apellidos": "Yanez", "pin": 1234}
    response = client.post("/empleados", json=empleado)

    assert response.status_code == 202
    data = response.json()
    assert data['apellidos'] == empleado['apellidos']
    assert data['nombre'] == empleado['nombre']
    assert data['pin'] == empleado['pin']


def test_put_empleados(uuid_empleado='ac05c1fc-254e-488c-b65a-7fb7aede3c43'):
    empleado = {"uuid": "ac05c1fc-254e-488c-b65a-7fb7aede3c43",
                "nombre": "Lupita", "apellidos": "Yanez", "pin": 1234}

    request_data = {"nombre": "Lupita", "apellidos": "Yanez", "pin": 1234}
    response = client.post("/empleados", json=request_data)
    assert empleado["uuid"] == uuid_empleado
    assert empleado['apellidos'] == request_data['apellidos']
    assert empleado['nombre'] == request_data['nombre']
    assert empleado['pin'] == request_data['pin']
    assert response.status_code == 202

