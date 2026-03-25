from fastapi import APIRouter

from app.schemas import FocusSessionOut


focus_session_router = APIRouter()

@focus_session_router.post("/focus_steps/{step_id}", status_code=201, response_model=FocusSessionOut)
def create_focus_session(step_id: int):
  ...