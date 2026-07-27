from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    done: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

tasks = [
    {
        "id": 1,
        "title": "Wake up!",
        "done": True
    },
    {
        "id": 2,
        "title": "Fix bed.",
        "done": False        
    },
    {
        "id": 3,
        "title": "Eat cereal.",
        "done": False       
    }
]


@app.get("/")
def read():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def read_status():
    return {
        "status": "ok"  
    }

@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns a list of all stored tasks."
)
def read_alltasks():
    return tasks

@app.get(
    "/tasks/{id}",
    summary="Get a task",
    description="Retrieves a task by its ID."
)
def read_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {id} not found"
    )

@app.post(
    "/tasks", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Creates a new task with a title."
)
def create_task(task: TaskCreate):
    if task.title.strip() == "":
       raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Bad Request. Title is required"
       )

    next_id = max(task["id"] for task in tasks) + 1

    new_task = {
        "id": next_id,
        "title": task.title,
        "done" : False
    }

    tasks.append(new_task)

    return new_task

@app.put(
    "/tasks/{id}",
    summary="Update a task",
    description="Updates the title or completion status of a task."
)
def update_task(id: int, update: TaskUpdate):
    if update.title is None and update.done is None:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="At least one field (title or done) must be provided."
       )

    for task in tasks:
        if task["id"] == id:
            if update.title is not None:
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task             

    raise HTTPException(
    status_code=404,
    detail=f"Task {id} not found"
    )

@app.delete(
    "/tasks/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return

    raise HTTPException(
    status_code=404,
    detail=f"Task {id} not found"
    )