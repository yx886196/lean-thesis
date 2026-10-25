@echo off
chcp 65001 >nul
set PATH=C:\Users\Lenovo\AppData\Local\Programs\MiKTeX\miktex\bin\x64;%PATH%

rem Build the PDF version of the blueprint.
rem We call xelatex directly (twice, for cross-references) instead of latexmk,
rem because MiKTeX's latexmk needs a Perl interpreter on Windows.

cd /d "%~dp0..\blueprint\src"
if not exist "..\print" mkdir "..\print"

echo [1/2] First pass...
xelatex -interaction=nonstopmode -output-directory="..\print" print.tex > nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] xelatex failed, see blueprint\print\print.log
    pause
    exit /b 1
)

echo [2/2] Second pass (cross-references)...
xelatex -interaction=nonstopmode -output-directory="..\print" print.tex > nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] xelatex failed, see blueprint\print\print.log
    pause
    exit /b 1
)

echo.
echo [OK] blueprint\print\print.pdf
pause
