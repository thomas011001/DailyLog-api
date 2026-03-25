from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.focus_step_router import focus_step_router
from app.routers.auth_router import auth_router
from app.routers.day_router import day_router
from app.routers.task_router import task_router
from app.routers.user_router import user_router

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SideBar    Day Section               Timer

# Usernaem   Mars 3 2025 - DayTitle
# ---------  ----------------------
# Day """"   [v] Task One
# Day """"   [v] Task Two
# Day """"   [-] Task Three
# Day """"   ----------------------
# Day """"   1. O (Focus Session)
# Day """"   2. coffee break
# Day """"   3. O O O
# Day """"   4. 30m Scrolling
# [  NEW  ]  5. O O O O

# App Flow

# Create New Account -
# Start New Day
# Set The Day Tasks
# Set The Day Steps

# Shared
# toggle step compelete  
# delete a step
# complete a step

# Focus
# create
# add, delete and toggle compelete sessions 

# Break
# create
# edit description

app.include_router(auth_router)
app.include_router(day_router)
app.include_router(task_router)
app.include_router(user_router)
app.include_router(focus_step_router)
