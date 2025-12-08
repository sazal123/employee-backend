# FastAPI HR Backend (Clean Architecture)

This is a ready-to-run FastAPI backend implementing HR-related APIs (Departments, Employees, etc.)
- PostgreSQL as database
- Docker + docker-compose
- Clean architecture: routers, services, repositories, models, schemas
- Auto-initialize database tables on startup (useful for development)

## Quick start

1. Build & run:
```bash
docker compose up --build
```

2. API will be available at: `http://localhost:8000`
3. Open docs at: `http://localhost:8000/docs`

## Notes
- Resume upload stores files inside the container at `/app/uploads` (for dev). In production use S3 or a proper storage volume.
- This repo is a starter scaffold. Additional endpoints and business logic should be implemented following the structure in `app/`.
