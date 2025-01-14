#Create Tunnel
ngrok http --url=admittedly-wired-halibut.ngrok-free.app 8000

#Run FastAPI
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
