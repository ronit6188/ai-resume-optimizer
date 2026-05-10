@echo off
echo ========================================
echo   AI Resume Optimizer - Starting...
echo ========================================
echo.

echo [1/2] Starting Backend server on port 8001...
start "Backend - FastAPI" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001"

echo [2/2] Starting Frontend server on port 3000...
start "Frontend - Next.js" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo   Servers are starting...
echo ========================================
echo.
echo URLs:
echo   - Frontend:    http://localhost:3000
echo   - Backend API: http://localhost:8001
echo   - API Docs:    http://localhost:8001/docs
echo   - Health:      http://localhost:8001/health
echo   - Readiness:   http://localhost:8001/health/ready
echo   - Liveness:    http://localhost:8001/health/live
echo.
echo Press any key to close this window (servers will keep running)...
pause >nul