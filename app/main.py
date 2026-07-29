from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from database import get_connection

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

@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns a list of all stored tasks."
)
def read_alltasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.get(
    "/tasks/{id}",
    summary="Get a task",
    description="Retrieves a task by its ID."
)
def read_task(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id =?", (id,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return JSONResponse(
        status_code=404,
        content={"error": "Task not found"}
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

@app.post(
    "/tasks", 
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Creates a new task with a title."
)
def create_task(task: TaskCreate):
    if task.title.strip() == "":
       return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Bad Request. Title is required"}
       )

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, 0))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return {
        "id": new_id,
        "title": task.title,
        "done": False
    }

@app.put(
    "/tasks/{id}",
    summary="Update a task",
    description="Updates the title or completion status of a task."
)
def update_task(id: int, update: TaskUpdate):
    if update.title is None and update.done is None:
        return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content="At least one field (title or done) must be provided."
       )

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id =?", (id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return JSONResponse(
        status_code=404,
        content={"error": "Task " + str(id) + " not found."}
        )
    if update.title is not None:
        cur.execute(
            """
            UPDATE tasks
            SET title = ?
            WHERE id = ?
            """,
            (update.title, id)
            )
    if update.done is not None:
        cur.execute(
            """
            UPDATE tasks
            SET done = ?
            WHERE id = ?
            """,
            (update.done, id)
            )  
    conn.commit()
    cur.execute("SELECT * FROM tasks WHERE id =?", (id,))
    row = cur.fetchone()
    conn.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }
          
@app.delete(
    "/tasks/{id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
def delete_task(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cur.fetchone()

    if row is None:
        conn.close()
        return JSONResponse(
        status_code=404,
        content={"error": "Task " + str(id) + " not found."}
        )
    cur.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return