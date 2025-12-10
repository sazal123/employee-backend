from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import os

from .db import init_db, engine
from .routers import departments, employees, job_positions, job_titles, work_locations, skill_types, skills, tags

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
app.include_router(job_titles.router, prefix='/job_titles',tags=['JobTitles'])
app.include_router(work_locations.router, prefix='/work_locations',tags=['WorkLocations'])
app.include_router(skill_types.router, prefix='/skill_types', tags=['SkillTypes'])
app.include_router(skills.router, prefix='/skills', tags=['Skills'])
app.include_router(tags.router, prefix='/tags', tags=['Tags'])

@app.on_event("startup")
def on_startup():
    # initialize DB (create tables)
    init_db()
    # create uploads dir if missing
    os.makedirs('uploads', exist_ok=True)
