@echo off
setlocal
cd /d "%~dp0"

set "PORT=8000"
set "URL=http://localhost:%PORT%/"

where python >nul 2>&1
if %errorlevel%==0 (
    set "PY_CMD=python"
) else (
    where py >nul 2>&1
    if %errorlevel%==0 (
        set "PY_CMD=py"
    ) else (
        echo Error: Python was not found in PATH.
        echo Please install Python 3 and ensure it is added to your system PATH.
        pause
        exit /b 1
    )
)

echo Starting archival documentation server at %URL%
echo Serving directory: %CD%
echo Press Ctrl+C in this window to stop the server.
echo.

start "" "%URL%"
%PY_CMD% -m http.server %PORT%
endlocal
