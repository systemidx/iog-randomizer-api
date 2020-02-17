@echo OFF
pip install -r requirements.txt --user
setlocal
SET DB_ENABLED=FALSE
SET DB_CONNECTIONSTRING=DefaultEndpointsProtocol=https;AccountName=iogr;AccountKey=QldJArxdM6YbzV+W6Ygcz1E5R9rLp6qH/D3C90ADka0doqqI5ggT8nQzCnKXQAnCuD2kNKyLoli2oey1MS+vrA==;EndpointSuffix=core.windows.net
SET DB_DATABASE_ID=iogr
SET DB_COLLECTION_ID=iogr-rockets
start python application.py
endlocal