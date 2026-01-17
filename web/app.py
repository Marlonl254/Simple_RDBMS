from fastapi import FastAPI, Query
from db.engine import db

app = FastAPI()

@app.get("/users")
def list_users(id: int | None = Query(None)):
    users = db.execute("SELECT * FROM users")
    if id is not None:
        users = [u for u in users if str(u["id"]) == str(id)]
    return users

@app.post("/users")
def create_user(id: int, name: str, active: bool = True):
    db.execute(f'INSERT INTO users VALUES ({id}, "{name}", {str(active).lower()})')
    return {"status": "created"}

@app.put("/users")
def update_user(id: int, name: str | None = None, active: bool | None = None):
    updates = []
    if name is not None:
        updates.append(f'name="{name}"')
    if active is not None:
        updates.append(f'active={str(active).lower()}')
    if updates:
        db.execute(f'UPDATE users SET {", ".join(updates)} WHERE id = {id}')
    return {"status": "updated"}

@app.delete("/users")
def delete_user(id: int):
    db.execute(f'DELETE FROM users WHERE id = {id}')
    return {"status": "deleted"}
