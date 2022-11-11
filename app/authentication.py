from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.database import database
from app.models import Comercio

security = HTTPBasic()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security), db: database.SessionLocal = Depends(get_db)):
    try:
        api_key = UUID(credentials.username)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key invalido",
        )
    comercio = db.query(Comercio).filter(
        Comercio.api_key == api_key, Comercio.activo == True).first()
    if not comercio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API Key no valido para comercio resgitrado",
        )
    return comercio, None
