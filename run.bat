@echo OFF
pip install -r requirements.txt --user
setlocal
SET DEBUG=TRUE
SET DB_ENABLED=FALSE

python application.py
endlocal