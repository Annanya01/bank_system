from fastapi import APIRouter, Depends, HTTPException, status, Request
from schemas import UserCreate, ShowUser
from sqlalchemy.orm import Session
from database import get_db
from models import User
from fastapi.templating import Jinja2Templates


router = APIRouter( include_in_schema=False )

templates = Jinja2Templates( directory="templates" )

@router.get("/")
def home_page(request : Request, msg:str = None):
    return templates.TemplateResponse( "general_pages/home.html", {"request" : request, "msg" : msg} )


