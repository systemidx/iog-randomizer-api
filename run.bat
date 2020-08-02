@echo OFF
pip install -r requirements.txt --user
setlocal
SET DB_ENABLED=FALSE
python application.py
endlocal