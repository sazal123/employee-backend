from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import os

from .db import init_db, engine
from .routers import departments, employees, job_positions

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# include routers
app.include_router(departments.router, prefix='/departments', tags=['Departments'])
app.include_router(employees.router, prefix='/employees', tags=['Employees'])
app.include_router(job_positions.router, prefix='/job_positions',tags=['JobPositions'])

@app.on_event("startup")
def on_startup():
    # initialize DB (create tables)
    init_db()
    # create uploads dir if missing
    os.makedirs('uploads', exist_ok=True)
