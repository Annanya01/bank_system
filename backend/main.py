from fastapi import FastAPI
from models import Base
from database import engine
from schemas import Settings
from routers import user, accounts, login

Base.metadata.create_all(bind = engine)

app = FastAPI()

@app.get("/api")
async def start() :
    return {"message" : "hello"}

app.include_router(user.router)
app.include_router(login.router)
app.include_router(accounts.router)

