
git clone https://github.com/Cosqui/dapp-fast-api.git

virtualenv env

source env/bin/active

pip install -r requirements.txt

uvicorn app.main:app --reload

// RUN TEST

otra terminal ejecutar a nivel del proyecto

pytest