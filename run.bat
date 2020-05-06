@echo OFF
pip install -r requirements.txt --user
setlocal
SET DB_ENABLED=TRUE
SET DB_CONNECTIONSTRING=mongodb://iogr-dev:1RQD7buxhZwT3QwNDIONq8dT2fcfMGnUcNXGQ2UUPGRiqvfkKGrPYBcAIi1VhCJWJOwChMJWVWUagCmHdaXizQ==@iogr-dev.mongo.cosmos.azure.com:10255/?ssl=true^&replicaSet=globaldb^&maxIdleTimeMS=120000^&appName=@iogr-dev@^&retrywrites=false
SET DB_DATABASE_ID=iogr-dev
SET DB_COLLECTION_ID=iogr-seeds
python application.py
endlocal