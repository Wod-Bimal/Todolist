# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Todo API")

# Pydantic models for data validation
class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# In-memory database simulation
todo_db = {}
id_counter = 1

# CREATE: Add a new todo
@app.post("/todos/", response_model=TodoItem, status_code=201)
def create_todo(todo: TodoCreate):
    global id_counter
    new_todo = TodoItem(
        id=id_counter,
        title=todo.title,
        description=todo.description,
        completed=False
    )
    todo_db[id_counter] = new_todo
    id_counter += 1
    return new_todo

# READ ALL: Get all todos
@app.get("/todos/", response_model=List[TodoItem])
def get_all_todos():
    return list(todo_db.values())

# READ ONE: Get a specific todo by ID
@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return todo_db[todo_id]

# UPDATE: Modify an existing todo
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo_update: TodoUpdate):
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    stored_todo = todo_db[todo_id]
    
    # Update only the fields that were provided in the request
    if todo_update.title is not None:
        stored_todo.title = todo_update.title
    if todo_update.description is not None:
        stored_todo.description = todo_update.description
    if todo_update.completed is not None:
        stored_todo.completed = todo_update.completed
        
    todo_db[todo_id] = stored_todo
    return stored_todo

# DELETE: Remove a todo
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todo_db:
        raise HTTPException(status_code=404, detail="Todo item not found")
    del todo_db[todo_id]
    return None

