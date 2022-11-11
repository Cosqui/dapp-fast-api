
from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


empleado = {
    "uuid": "6f184525-f881-4dce-bf6d-3ff1225a0955",
    "nombre": "Palomita",
    "pin": "125",
    "fecha_creacion": "2022-11-11T00:08:06",
    "apellidos": "Yañez",
    "id": 4,
    "comercio_id": 1,
    "activo": True
}


def test_get_empleados_not_auth():
    response = client.get(
        "/empleados")
    assert response.status_code == 401


def test_get_empleados():
    authUser = ('3d32f2cb-b2de-4038-bb67-01f6c2fd4513', '')
    response = client.get(
        "/empleados", auth=authUser)
    assert response.status_code == 200


def test_post_empleados(uuid_empleado='ac05c1fc-254e-488c-b65a-7fb7aede3c43'):
    authUser = ('3d32f2cb-b2de-4038-bb67-01f6c2fd4513','')
    new_user = {"nombre": "Lupita", "apellidos": "Yanez", "pin": "1234"}
    response = client.post("/empleados", json=new_user, auth=authUser)

    assert uuid_empleado is not None
    data = response.json()
    assert new_user['apellidos'] == new_user['apellidos']
    assert data['nombre'] == new_user['nombre']
    assert data['pin'] == new_user['pin']
    assert response.status_code == 201


def test_put_empleados():
    authUser = ('3d32f2cb-b2de-4038-bb67-01f6c2fd4513', '')
    update_empleado = {"nombre": "Nombre Acutalizado",
                       "apellidos": "Lopez", "pin": "222"}
    response = client.put("/empleados", json=update_empleado, auth=authUser,
                          params={'uuid_empleado': '6f184525-f881-4dce-bf6d-3ff1225a0955'})
    assert response.status_code == 201 or response.status_code == 404


def test_delete_empleados():
    authUser = ('3d32f2cb-b2de-4038-bb67-01f6c2fd4513', '')
    response = client.delete("/empleados", auth=authUser,
                             params={'uuid_empleado': 'a9d3160c-f429-4d7d-9742-7f837d9d8521'})
    assert response.status_code == 200 or response.status_code == 404
