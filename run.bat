@echo OFF
pip install -r requirements.txt --user
setlocal
SET DB_ENABLED=FALSE
SET DB_CONNECTIONSTRING=
SET DB_DATABASE_ID=
SET DB_COLLECTION_ID=
start python application.py
endlocal