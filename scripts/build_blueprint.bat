@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set GIT_PYTHON_GIT_EXECUTABLE=F:\CodeBuddy\tools\git\cmd\git.exe
set PATH=F:\CodeBuddy\tools\texshim;C:\Program Files\Graphviz\bin;F:\CodeBuddy\tools\git\cmd;%USERPROFILE%\.elan\bin;%PATH%

cd /d "%~dp0.."

echo ============================================
echo  Building blueprint web version
echo ============================================
leanblueprint web

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] build failed
    pause
    exit /b 1
)

echo.
echo [OK] Generated: blueprint\web\index.html
echo.
echo Tip: start a local server with
echo   python -m http.server 8765 --directory blueprint\web
echo then open http://localhost:8765/
pause
