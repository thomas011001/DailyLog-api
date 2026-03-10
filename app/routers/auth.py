from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.repo.user import UserRepo
from app.utiles import hash_password

# sign up [V]
# login [ ]
# logout [ ]
# refresh [ ]

# user in schema 
class CreateUser(BaseModel):
  username: str = Field(min_length=3)
  password: str = Field(min_length=5) 

class UserOut(BaseModel):
  username: str

auth_router = APIRouter()

@auth_router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
  repo = UserRepo(db)

  # if repo.username_exists(user.username):
  #   raise HTTPException(status.HTTP_409_CONFLICT, "This username is taken .")
  
  hashed_password = hash_password(user.password)

  try:
    new_user = repo.create_user({"username": user.username, "password_hash": hashed_password})

  except IntegrityError:
    raise HTTPException(status.HTTP_409_CONFLICT, "This username is taken .")

  except Exception:
      db.rollback()
      raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Could not create the user.")
      
  return new_user
  