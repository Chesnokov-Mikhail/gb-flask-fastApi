# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок
# и описание. Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
#
# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
#
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import enum
from typing import Optional
from fastapi.openapi.utils import get_openapi

app = FastAPI(openapi_url="/api/v1/openapi.json")

class Status(enum.Enum):
    completed: str = "completed"
    not_completed: str = "not completed"

class BaseTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None

    def __repr__(self):
        return f"BaseTask({self.title},{self.description},{self.status})"

class Task(BaseTask):
    id: int
    title: str
    description: str
    status: Status = Status.not_completed

    def __repr__(self):
        return f"Task({self.id},{self.title},{self.description},{self.status})"

tasks_list: list[Task] = []

@app.get("/tasks/", response_model=list[Task], status_code=status.HTTP_200_OK)
async def get_all_task():
    global tasks_list
    if tasks_list:
        return [task for task in tasks_list]
    else:
        raise HTTPException(status_code=404, detail="List task is null")

@app.get("/tasks/{id}", response_model=Task, status_code=status.HTTP_200_OK)
async def get_task(id: int):
    global tasks_list
    for i in range(len(tasks_list)):
        if tasks_list[i].id == id:
            return tasks_list[i]
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def add_task(task: Task):
    global tasks_list
    for i in range(len(tasks_list)):
        if tasks_list[i].id == task.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Task id={task.id} exist")
    tasks_list.append(task)
    return task

@app.put("/tasks/{id}", response_model=Task, status_code=status.HTTP_202_ACCEPTED)
async def put_task(id: int, task: BaseTask):
    global tasks_list
    for i in range(len(tasks_list)):
        if tasks_list[i].id == id:
            if task.title:
                tasks_list[i].title = task.title
            if task.description:
                tasks_list[i].description = task.description
            if task.status:
                tasks_list[i].status = task.status
            return tasks_list[i]
    raise HTTPException(status_code=404, detail=f"Task id={id} not found, not update")

@app.delete("/tasks/{id}", response_model=Task, status_code=status.HTTP_200_OK)
async def del_task(id: int):
    global tasks_list
    for i in range(len(tasks_list)):
        if tasks_list[i].id == id:
            task = tasks_list.pop(i)
            return task
    raise HTTPException(status_code=404, detail=f"Task id={id} not deleted")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(title="Custom title",
                                 version="1.0.0",
                                 description="This is a very custom OpenAPI schema",
                                 routes=app.routes,
                                 )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi