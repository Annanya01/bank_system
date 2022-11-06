# import os as _os

# import dotenv as _dotenv
# import jwt 
# import sqlalchemy.orm as _orm
# import passlib.hash as _hash
# import email_validator as _email_check
# import fastapi as _fastapi
# import fastapi.security as _security
# from werkzeug.security import generate_password_hash,check_password_hash

# from models import User
# from schemas import LoginModel
# import models as _models
# from config import settings


# async def authenticate_user(email: str, password: str, db: _orm.Session):
#     user = await db.query(User).filter(User.email == email).first()

#     if not user:
#         return False
    
#     if not user.check_password_hash(password):
#         return False

#     return user

# async def create_token(login: LoginModel):
#     print(login.dict())
#     user_dict = login.dict()

#     token = jwt.encode(user_dict, settings.SECRET_KEY)

#     return dict(access_token=token, token_type="bearer")