@echo OFF
pip install -r requirements.txt --user
setlocal
SET DEBUG=TRUE
SET DB_AUTHDB=iogr
SET DB_COLLECTION_ID=seeds
SET DB_DATABASE_ID=iogr
SET DB_ENABLED=FALSE
SET DB_HOST=
SET DB_PASSWORD=
SET DB_PORT=
SET DB_USERNAME=

python application.py
endlocal