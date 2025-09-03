from fastapi import FastAPI
from api.routes import api_router
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)

# Healt endpoint
@app.get("/")
def root():
    return {"msg": "GridDFS api is running"}