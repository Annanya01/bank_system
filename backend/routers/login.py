from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from database import get_db
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash,check_password_hash

from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

from models import User
from schemas import LoginModel

router = APIRouter()

session=SessionLocal(bind=engine)
# db: Session = Depends(get_db)

def func(user1 : LoginModel,access_token:str):
    print(user1)
    update_user = session.query(User).filter(User.email == user1.email).first()
    print(update_user)
    update_user.token= access_token
    session.commit()

# USER LOGIN
@router.post('/login',status_code=200)
def login(request :LoginModel, Authorize:AuthJWT=Depends(), db: Session = Depends(get_db)):
    """
    ## Registered user can login using this route
    You need To Enter:
     - email : str
     - password : str
    """

    db_user = db.query(User).filter(User.email == request.email).first()
    print(db_user)
    if db_user and check_password_hash(db_user.password , request.password):
        print(db_user.email)

        #Generate JWT Token
        access_token=Authorize.create_access_token(subject=db_user.email,expires_time=timedelta(days=1))
        print(access_token)
        refresh_token=Authorize.create_refresh_token(subject=db_user.email,expires_time=timedelta(days=1))
        func(request ,access_token)
        response={
            "message":"Login Successfull",
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code=400,detail="Invalid Email or Password")





# async def login_service(login: LoginModel, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == login.email).first()

#     if user is not None:
#         if not check_password_hash(user.password ,login.password):
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Password")
#         return JWTRepo(data= {"email" : user.email}).generate_token()
#     raise HTTPException(status_code=404, detail="Username not found !")

# @router.post('/login', response_model= ResponseModel)
# async def login(request_body = LoginModel):
#     token = await login_service(request_body)
#     return ResponseModel(detail="Successfully login", result = {"token_type": "Bearer", "access_token": token})

# @router.post("/login/token")
# def retrieve_token_after_authentication(response : Response, form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
#     user = db.query(User).filter(User.email == form_data.username).first()
#     print(user.email)

#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Username")
#     if not check_password_hash(user.password ,form_data.password ):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Password")

#     data = {'sub' : form_data.username}
#     print(data)
#     jwt_token = jwt.encode(data, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
#     # response.set_cookie(key="access_token", value=f"Bearer {jwt_token}", httponly=True)

#     return {'access_token' : jwt_token, 'token_type' : 'bearer'}

# def authenticate_user(email: str, password: str, db: Session = Depends()):
#     user = db.query(User).filter(User.email == email).first()
#     print(user.email)
#     print(user.password)

#     if not user:
#         return False

#     if not check_password_hash(user.password, password):
#         return False

#     return user

# async def create_token(user: User):
#     user_obj = LoginModel.from_orm(user)

#     user_dict = user_obj.dict()
#     print(user_dict)
#     del user_dict["date_created"]

#     token = jwt.encode(user_dict, settings.SECRET_KEY)

#     return dict(access_token=token, token_type="bearer")

# @router.post("/api/token")
# def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = authenticate_user(email=form_data.username, password=form_data.password, db=db)

#     print(user)
#     if not user:
#         raise HTTPException(
#             status_code=401, detail="Invalid Credentials")

#     return create_token(user=user)

# def func(user1:LoginModel,access_token:str, db: Session = Depends(get_db)):
#     user_to_update = db.query(User).filter(User.email==user1.email).first()
#     user_to_update.token= access_token
#     db.commit()

# @router.post('/login',status_code=200)
# async def login(user:LoginModel,Authorize:AuthJWT=Depends(),db: Session = Depends(get_db)):

#     """
#     ## Registered user can login using this route
#     You need To Enter:
#      - email : str
#      - password : str
#     """

#     db_user=db.query(User).filter(User.email== user.email).first()
#     if db_user and check_password_hash(db_user.password,user.password):
#         access_token=Authorize.create_access_token(subject=db_user.email,expires_time=timedelta(days=1))
#         refresh_token=Authorize.create_refresh_token(subject=db_user.email,expires_time=timedelta(days=1))
#         func(user,access_token)
#         response={
#             "message":"Login Successfull",
#             "access":access_token,
#             "refresh":refresh_token
#         }

#         return jsonable_encoder(response)
    
#     raise HTTPException(status_code=400,detail="Invalid Email or Password")
