from fastapi import FastAPI
from api.routes import api_router

app = FastAPI(title="GridDFS API")
app.include_router(api_router)

# Healt endpoint
@app.get("/")
def root():
    return {"msg": "GridDFS api is running"}