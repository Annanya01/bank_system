from http.client import responses
from sqlite3 import IntegrityError
from sys import api_version
from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import User
from models import Account as AccountModel
# from hashing import Hasher
from schemas import ShowUser
import random

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get('/register')
def registration(request: Request):
    return templates.TemplateResponse("general_pages/register.html", {"request" : request})

@router.post('/register', response_model=ShowUser)
async def registration(request: Request, db:Session = Depends(get_db)):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    account_no = random.randint(100000000000,999999999999)
    print(form.get(account_no))
    errors = []

    if len(password) < 4:
        errors.append("Password length too short")
        return templates.TemplateResponse("general_pages/register.html", {"request": request, "errors": errors})
    user = User(username = username, password = password, account_no = account_no)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        account = AccountModel(user_id=user.id, account_no = user.account_no)
        print(account)
        db.add(account)
        db.commit()
        db.refresh(account)
        # Redirecting to home page
        # return responses.RedirectResponse('/', status_code = status.HTTP_200_OK)
        #Redirecting to homepage with SuccessfulResponse query parameter
        print(user.id)
        return responses.RedirectResponse("/?msg=Successfuly registered", status_code = status.HTTP_302_FOUND)

# integrity errors : when unique constriant is voilated
    except IntegrityError: 
        errors.append("Username already exists")
        return templates.TemplateResponse("general_pages/register.html", {"request": request, "errors": errors})
