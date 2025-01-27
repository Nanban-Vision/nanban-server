#Create Tunnel using ngrok
ngrok http --url=admittedly-wired-halibut.ngrok-free.app 8000

#Run FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
