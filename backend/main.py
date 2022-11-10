
from fastapi import FastAPI
from database import engine
from models import Base
from routers import user, accounts, login
from fastapi_jwt_auth import AuthJWT
from schemas import Settings
# from webapps.routers import user as web_user
# from webapps.routers import auth as web_auth
# from webapps.routers import homepage as web_homepage
# from webapps.routers import accounts, check_balance

# adding CORS headers
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind = engine)

app = FastAPI()

# adding CORS urls
origins = [
        '*',
]
# add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@AuthJWT.load_config
def get_config():
    return Settings()

@app.get('/api')
async def root():
    return {"msg" : "Connected with backend"}

app.include_router(user.router)
app.include_router(accounts.router)
app.include_router(login.router)
# app.include_router(web_auth.router)
# app.include_router(web_user.router)
# app.include_router(web_homepage.router)
# app.include_router(check_balance.router)



