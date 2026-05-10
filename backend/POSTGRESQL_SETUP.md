# PostgreSQL Setup Guide

## Prerequisites
- PostgreSQL 14+ installed on your system

## Quick Start (Windows)

### 1. Start PostgreSQL Service
```powershell
# If using PostgreSQL installed as a service
Start-Service postgresql-x64-14

# Or start manually
& "C:\Program Files\PostgreSQL\14\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\14\data" start
```

### 2. Create Database
```powershell
# Connect to PostgreSQL
& "C:\Program Files\PostgreSQL\14\bin\psql.exe" -U postgres

# In psql, create database:
CREATE DATABASE ai_resume_optimizer;

# Exit psql
\q
```

### 3. Configure Environment
The `.env` file is already configured:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_resume_optimizer
```

If you need a different password, update it:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ai_resume_optimizer
```

### 4. Run Migrations
```powershell
cd backend
alembic upgrade head
```

### 5. Start Backend
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Using Docker (Alternative)

```powershell
# Run PostgreSQL in Docker
docker run --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=ai_resume_optimizer -p 5432:5432 -d postgres:14

# Then run migrations
cd backend
alembic upgrade head
```

## Troubleshooting

### Connection Refused
- Check PostgreSQL service is running: `Get-Service | Where-Object {$_.Name -like "*postgres*"}`
- Verify port 5432 is not blocked

### Authentication Failed
- Edit `pg_hba.conf` to allow password authentication
- Or modify `.env` with correct credentials

### Database Already Exists
```sql
DROP DATABASE ai_resume_optimizer;
CREATE DATABASE ai_resume_optimizer;
```

## Quick Test (SQLite Fallback)

If PostgreSQL is not available, temporarily use SQLite:
```
# In .env
DATABASE_URL=sqlite:///./resume_optimizer.db
```
Then the app will create tables automatically on startup.