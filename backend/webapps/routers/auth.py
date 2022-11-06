
from fastapi import APIRouter, Request, Depends, Response, status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from config import settings
from models import User
from database import get_db
from hashing import Hasher
from jose import jwt
from config import settings

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/login')
def login(request: Request):
    return templates.TemplateResponse('general_pages/login.html', {'request':request})

@router.post('/login')
async def login(response:Response, request: Request, db:Session=Depends(get_db)):
    form = await request.form()
    username = form.get('username')
    print(username)
    password = form.get('password')
    print(password)
    errors = []
    if not username:
        errors.append('Please enter valid username')
    if not password:
        errors.append('Please enter password')
    if len(password) < 4:
        errors.append('Password too short')
    try:
        user = db.query(User).filter(User.username==username).first()
        print(user)
        if user is None:
            errors.append('Username does not exists')
            return templates.TemplateResponse('general_pages/login.html', {'request':request, 'errors':errors})
        else:
            print('inside else')
            # user = db.query(User).all().first()
            if Hasher.verify_password(password, user.password):
                data = {'sub': username}
                jwt_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
                msg = 'Login Successful'
                # user_details = user.id
                response = templates.TemplateResponse(
                    "general_pages/homepage.html", {"request": request, "msg": msg}
                )
                response.set_cookie(
                    key="access_token", value=f"Bearer {jwt_token}", httponly=True
                )
                return response
            else:
                errors.append("Invalid password")
                return templates.TemplateResponse("general_pages/login.html", {"request": request, "errors": errors})

    except:
        errors.append('Something went wrong !!')
        return templates.TemplateResponse('general_pages/login.html', {'request':request, 'errors':errors})

