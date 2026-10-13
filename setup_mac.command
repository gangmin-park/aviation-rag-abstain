#!/bin/bash
# aviation-rag-abstain : macOS setup (Week 0)
# Run in Terminal:  bash ~/Documents/aviation-rag-abstain/setup_mac.command
cd "$(dirname "$0")" || exit 1
echo "================================================"
echo " aviation-rag-abstain : macOS setup (Week 0)"
echo "================================================"

fail() { echo "[X] $1"; echo "    Copy the error text above and send it to Claude."; exit 1; }

# ---- 1. Python: prefer 3.10-3.12 (keeps the Week 4 PyTorch option open), accept 3.9+ ----
PY=""
for c in python3.12 python3.11 python3.10 python3 python; do
  if command -v "$c" >/dev/null 2>&1 && \
     "$c" -c 'import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] <= (3,12) else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done
if [ -z "$PY" ]; then
  for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1 && \
       "$c" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3,9) else 1)' 2>/dev/null; then
      PY="$c"
      echo "[!] Using $("$c" --version 2>&1). Fine for Weeks 0-3; Week 4 may need Python 3.10-3.12."
      break
    fi
  done
fi
[ -n "$PY" ] || fail "Python 3.9+ not found. Install Python 3.12 from https://www.python.org/downloads/macos/ and run this again."
echo "[OK] $("$PY" --version 2>&1)  ($(command -v "$PY"))"

# ---- 2. Virtual environment ----
if [ -x ".venv/bin/python" ]; then
  echo "[OK] .venv already exists"
else
  echo "[..] Creating virtual environment .venv"
  "$PY" -m venv .venv || fail "Could not create .venv"
fi
# shellcheck disable=SC1091
source .venv/bin/activate || fail "Could not activate .venv"

# ---- 3. Core packages ----
echo "[..] Installing packages from requirements.txt"
python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt || fail "pip install failed"
echo "[OK] Packages installed"

# ---- VS Code: point the editor at .venv and enable the pytest test explorer ----
if [ ! -f ".vscode/settings.json" ]; then
  mkdir -p .vscode
  cat > .vscode/settings.json <<'JSON'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests"]
}
JSON
  echo "[OK] VS Code settings created (.vscode/settings.json)"
fi

# ---- 4. Tests ----
echo
echo "[..] Running tests. 9 FAILED with NotImplementedError is EXPECTED right now."
echo "     Your job from Week 2 on: make them pass one by one."
python -m pytest -q
echo

# ---- 5. Git ----
if ! xcode-select -p >/dev/null 2>&1; then
  echo "[!] Git (Xcode Command Line Tools) is not installed."
  echo "    Run:  xcode-select --install   then run this script again."
  echo "    (The Python environment is already set up; only the Git step was skipped.)"
  exit 0
fi
if [ -z "$(git config --global user.name)" ]; then
  read -r -p "Name to show on your Git commits (e.g. Gangmin Park): " GN
  git config --global user.name "$GN"
fi
if [ -z "$(git config --global user.email)" ]; then
  echo "Tip: GitHub Settings > Emails shows a private 'noreply' address you can use here."
  read -r -p "Email for your Git commits: " GE
  git config --global user.email "$GE"
fi
if [ -d ".git" ]; then
  echo "[OK] Git repository already initialised"
else
  git init -b main >/dev/null && git add . && \
  git commit -q -m "Initial scaffold (setup utility and test specs)" && \
  echo "[OK] First local commit created"
fi

echo
echo "================================================"
echo " Setup finished. Next (Week 0):"
echo "  1. Open this folder in VS Code:  code ~/Documents/aviation-rag-abstain"
echo "     (or VS Code > File > Open Folder)"
echo "  2. Fill the two FAA URLs in src/download.py, then run:  python -m src.download"
echo "  3. Create an EMPTY public repo on github.com named aviation-rag-abstain"
echo "     (no README, no .gitignore), then in the VS Code terminal run:"
echo "       git remote add origin https://github.com/YOUR_ID/aviation-rag-abstain.git"
echo "       git push -u origin main"
echo "================================================"
