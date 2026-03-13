import datetime
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
import jwt
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.dependancies import get_user_repo
from app.models import User
from app.repo.user_repo import UserRepo
from app.utiles import hash_password, verify_password

load_dotenv()

# sign up [V]
# login [V]
# logout [ ]
# refresh [ ]

# user in schema 
class CreateUser(BaseModel):
  username: str = Field(min_length=3)
  password: str = Field(min_length=5) 

class UserOut(BaseModel):
  id: int
  username: str

class Credentials(BaseModel):
  username:str = Field(min_length=1)
  password:str = Field(min_length=1)

auth_router = APIRouter()

@auth_router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, repo: UserRepo = Depends(get_user_repo)):

  hashed_password = hash_password(user.password)

  try:
    new_user = repo.create_user(User(username=user.username, password_hash=hashed_password))
  except IntegrityError:
    raise HTTPException(status.HTTP_409_CONFLICT, "This username is taken.")

  except Exception:
      raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not create the user.")
      
  return new_user
  
@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: Credentials, repo: UserRepo = Depends(get_user_repo)):
  user = repo.get_user_by_username(credentials.username)
  if not user:
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid username or password")
  
  correct_password = verify_password(credentials.password, user.password_hash)
  if not correct_password:
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid username or password")
  
  token = user.token

  return {"token": token}