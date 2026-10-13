@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
echo ================================================
echo  aviation-rag-abstain : Windows setup (Week 0)
echo ================================================
echo.

rem ---- 1. Python 3.10+ ----
set "PY=python"
where py >nul 2>nul && set "PY=py -3"
%PY% --version >nul 2>nul
if errorlevel 1 goto :nopython
%PY% -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)"
if errorlevel 1 goto :oldpython
for /f "delims=" %%v in ('%PY% --version') do echo [OK] %%v

rem ---- 2. Virtual environment ----
if exist ".venv\Scripts\python.exe" (
  echo [OK] .venv already exists
) else (
  echo [..] Creating virtual environment .venv
  %PY% -m venv .venv
  if errorlevel 1 goto :fail
)
call ".venv\Scripts\activate.bat"

rem ---- 3. Packages (first run downloads ~1 GB incl. PyTorch; can take 5-15 min) ----
echo [..] Installing packages from requirements.txt
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail
echo [OK] Packages installed

rem ---- 4. Tests ----
echo.
echo [..] Running tests. 9 FAILED with NotImplementedError is EXPECTED right now.
echo      Your job from Week 2 on: make them pass one by one.
python -m pytest -q
echo.

rem ---- 5. Git ----
where git >nul 2>nul
if errorlevel 1 goto :nogit
set "GN="
for /f "delims=" %%i in ('git config --global user.name 2^>nul') do set "GN=%%i"
if not defined GN (
  set /p "GN=Name to show on your Git commits (e.g. Gangmin Park): "
  git config --global user.name "!GN!"
)
set "GE="
for /f "delims=" %%i in ('git config --global user.email 2^>nul') do set "GE=%%i"
if not defined GE (
  echo Tip: GitHub Settings ^> Emails shows a private "noreply" address you can use here.
  set /p "GE=Email for your Git commits: "
  git config --global user.email "!GE!"
)
if exist ".git" (
  echo [OK] Git repository already initialised
) else (
  git init -b main
  git add .
  git commit -m "Initial scaffold (setup utility and test specs)"
  echo [OK] First local commit created
)
echo.
echo ================================================
echo  Setup finished. Next (Week 0):
echo   1. Open this folder in VS Code
echo   2. Fill the two FAA URLs in src\download.py, then run:  python -m src.download
echo   3. Create an EMPTY public repo on github.com named aviation-rag-abstain
echo      (no README, no .gitignore), then in the VS Code terminal run:
echo        git remote add origin https://github.com/YOUR_ID/aviation-rag-abstain.git
echo        git push -u origin main
echo ================================================
pause
exit /b 0

:nopython
echo [X] Python not found. Install Python 3.10+ from https://www.python.org/downloads/
echo     and tick "Add python.exe to PATH" during install. Then run this file again.
pause
exit /b 1
:oldpython
echo [X] Python 3.10 or newer is required. Install a newer version from python.org.
pause
exit /b 1
:nogit
echo [!] Git not found. Install from https://git-scm.com/download/win , then run this file again.
echo     (Python environment is already set up; only the Git step was skipped.)
pause
exit /b 0
:fail
echo [X] A step failed. Copy the red error text above and send it to Claude.
pause
exit /b 1
