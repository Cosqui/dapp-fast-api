
from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)

# empleado a actualizar o eliminaar
emp = {
    "apellidos": "Yañez",
    "id": 1,
    "comercio_id": 1,
    "activo": True,
    "uuid": "3add8406-e4a1-45d4-9eeb-1cb8a81a58cd",
    "nombre": "Palomita",
    "pin": "125",
    "fecha_creacion": "2022-11-15T04:10:36"
}


def test_get_empleados_not_auth():
    response = client.get(
        "/empleados")
    assert response.status_code == 401


def test_get_empleados():
    authUser = ('f050312c-02d3-409f-a105-594f67cbe878', '')
    response = client.get(
        "/empleados", auth=authUser)
    assert response.status_code == 200

def test_post_empleados_not_auth():
    new_user = {"nombre": "Alonso", "apellidos": "Yanez", "pin": "134"}
    response = client.post("/empleados", json=new_user)
    assert response.status_code == 401


def test_post_empleados():
    authUser = ('f050312c-02d3-409f-a105-594f67cbe878','')
    new_user = {"nombre": "Lupita", "apellidos": "Yanez", "pin": "1234"}
    response = client.post("/empleados", json=new_user, auth=authUser)

    data = response.json()
    assert data['apellidos'] != ""
    assert data['nombre'] != ""
    assert data['pin'] != ""
    assert response.status_code == 201

def test_post_empleados_integrity():
    authUser = ('f050312c-02d3-409f-a105-594f67cbe878','')
    new_user = {"nombre": "Lupita", "apellidos": "Yanez", "pin": "1234"}
    response = client.post("/empleados", json=new_user, auth=authUser)

    assert response.status_code == 409


def test_put_empleados_not_auth():
    update_empleado = {"nombre": "Nombre Acutalizado",
                       "apellidos": "Lopez", "pin": "222"}
    response = client.put(
        "/empleados", json=update_empleado,
                          params={'uuid_empleado': '6f184525-f881-4dce-bf6d-3ff1225a0955'})
    assert response.status_code == 401

def test_put_empleados():
    authUser = ('f050312c-02d3-409f-a105-594f67cbe878', '')
    update_empleado = {"nombre": "Nombre Acutalizado",
                       "apellidos": "Lopez", "pin": "222"}
    response = client.put("/empleados", json=update_empleado, auth=authUser,
                          params={'uuid_empleado': '6f184525-f881-4dce-bf6d-3ff1225a0955'})
    assert response.status_code == 201

def test_put_empleados_not_uuid():
    authUser = ('f050312c-02d3-409f-a105-594f67cbe878', '')
    update_empleado = {"nombre": "Nombre Acutalizado",
                       "apellidos": "Lopez", "pin": "222"}
    response = client.put("/empleados", json=update_empleado, auth=authUser)
    assert response.status_code == 404

def test_delete_empleados_not_auth():
    response = client.delete("/empleados",
                             params={'uuid_empleado': 'adea6eec-16ed-4326-a7a9-3bc11d0c7096'})
    assert response.status_code == 401


def test_delete_empleados():
    authUser = ('f050312c-02d3-409f-a105-594f67cbe878', '')
    response = client.delete("/empleados", auth=authUser,
                             params={'uuid_empleado': '37b31def-8e01-45df-aa38-287a0e0db0a2'})
    assert response.status_code == 200 

def test_delete_empleados_not_uuid():
    authUser = ('f050312c-02d3-409f-a105-594f67cbe878', '')
    response = client.delete("/empleados", auth=authUser)
    assert response.status_code == 404 
