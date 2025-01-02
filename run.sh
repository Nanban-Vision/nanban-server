#Create Tunnel
ssh -R nanban.serveo.net:80:localhost:8000 serveo.net

#Run FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
