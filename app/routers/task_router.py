from fastapi import APIRouter, Depends, HTTPException, status

from app.dependancies import get_current_user, get_task_service
from app.exception import DayNotFoundError, ForbiddenDayAccessError, TaskNotFoundError
from app.schemas import CreateTask, TaskOut, UpdateTask
from app.services.task_service import TaskService


task_router = APIRouter()


@task_router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: CreateTask,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    try:
        task = service.create_task(user_id=current_user["id"], payload=payload)
        return task
    except DayNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Day not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@task_router.put(
    "/tasks/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK
)
def edit_task(
    task_id: int,
    payload: UpdateTask,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    try:
        task = service.edit_task(
            task_id=task_id, user_id=current_user["id"], payload=payload
        )
        return task
    except TaskNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )


@task_router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    try:
        service.delete_task(task_id=task_id, user_id=current_user["id"])
    except TaskNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    except ForbiddenDayAccessError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Forbidden.")
    except Exception:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error."
        )

    return {"detail": "Task deleted."}
