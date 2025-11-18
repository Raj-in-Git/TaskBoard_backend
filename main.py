from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc
import os
from dotenv import load_dotenv
import datetime
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables
load_dotenv()

app = FastAPI(title="TaskBoard - Backend")

# ✅ Allow frontend (React/HTML) access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database connection
def get_connection():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={os.getenv("DB_SERVER")};'
        f'DATABASE={os.getenv("DB_NAME")};'
        f'UID={os.getenv("DB_USER")};'
        f'PWD={os.getenv("DB_PASSWORD")};'
        'TrustServerCertificate=yes;'
    )
    return pyodbc.connect(conn_str)

# Pydantic model for validation
class Task(BaseModel):
    taskname : str
    details : str
    status : str

# Pydantic model for validation
class Update(BaseModel):
    task : str
    update : str
    efforts : int

# ✅ Read all tasks
@app.get("/tasks")
def get_tasks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("select * from task;")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "taskname": row[1],
                "details": row[2],
                "created_at": row[3],
                "updated_at": row[4],
                "status": row[5],

            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/tasks/active")
def active_tasks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("select count(taskname) from task where status = 'Active';")
        rows = cursor.fetchall()
        result = ''
        for row in rows:
            result = row[0]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/tasks/active/name")
def active_tasks():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("select taskname from task where status = 'Active';")
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "taskname": row[0]
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ✅ Create (Insert) task
@app.post("/tasks")
def create_task(task: Task):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now()
        query = """
        INSERT INTO task (taskname, details, created_at, updated_at, status)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (task.taskname, task.details, now, now,"Active"))
        conn.commit()
        return {"message": "Task inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Update task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now()
        query = """
        UPDATE task
        SET taskname = ?, details = ?, updated_at = ?, status = ?
        WHERE id = ?
        """
        cursor.execute(query, (task.taskname, task.details, now, task.status, task_id))
        conn.commit()
        return {"message": "Task updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Delete task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM task WHERE id = ?", (task_id,))
        conn.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


@app.get("/getUpdates")
def get_updates():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT *
        FROM updates
        ORDER BY updated_time DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "Updated_Time": row[1],
                "Task_Name": row[2],
                "Update": row[3],
                "Efforts": row[4]
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Create (Insert) task
@app.post("/addUpdates")
def add_updates(task: Update):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now()
        query = """
        INSERT INTO updates (Task_name, [update], Efforts)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (task.task, task.update, task.efforts))
        conn.commit()
        return {"message": "Task inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Update updates
@app.put("/editUpdates/{update_id}")
def edit_updates(update_id: int, task: Update):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now()
        query = """
        UPDATE updates
        SET task_name = ?, updates = ?, efforts = ?
        WHERE id = ?
        """
        cursor.execute(query, (task.taskname, task.update, task.efforts, update_id))
        conn.commit()
        return {"message": "Task updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# ✅ Delete task
@app.delete("/deleteUpdates/{update_id}")
def delete_updates(update_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM updates WHERE id = ?", (update_id,))
        conn.commit()
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
