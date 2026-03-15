from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth_router import auth_router
from app.routers.day_router import day_router
from app.routers.note_router import note_router
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


app.include_router(auth_router)
app.include_router(day_router)
app.include_router(task_router)
app.include_router(note_router)
app.include_router(user_router)