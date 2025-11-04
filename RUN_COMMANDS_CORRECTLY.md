# ✅ How to Run Commands Correctly

## Problem

You tried to run two commands together. They need to be run **separately**.

## Solution: Run Commands One at a Time

### Option 1: Use Command Prompt (CMD) - Easiest!

**Open Command Prompt (not PowerShell):**

1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to your project:
   ```cmd
   cd E:\youssef_anas\game-boosters-main
   ```

**Then run commands one by one:**

```cmd
REM Step 1: Activate virtual environment
venv\Scripts\activate.bat

REM Step 2: Verify setup
python verify_realtime_setup.py

REM Step 3: Apply migrations
python manage.py migrate --noinput

REM Step 4: Start server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

### Option 2: Use PowerShell (Fix Execution Policy First)

**Fix PowerShell execution policy:**

1. Open PowerShell as Administrator
2. Run this command:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Type `Y` and press Enter

**Then run commands one by one:**

```powershell
# Step 1: Activate virtual environment
venv\Scripts\activate

# Step 2: Verify setup
python verify_realtime_setup.py

# Step 3: Apply migrations
python manage.py migrate --noinput

# Step 4: Start server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

### Option 3: Continue Without Virtual Environment (Simplest)

Since packages are already installed globally, you can skip activating the venv:

**In PowerShell, run these commands one by one:**

```powershell
# Step 1: Verify setup
python verify_realtime_setup.py

# Step 2: Apply migrations
python manage.py migrate --noinput

# Step 3: (Optional) Start Redis
docker compose up -d redis

# Step 4: Start server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Important: Run Commands Separately!

**WRONG:**
```powershell
venv\Scripts\activate.batify_realtime_setup.py
```

**CORRECT:**
```powershell
# First command
venv\Scripts\activate.bat

# Then wait for (venv) to appear, then run:
python verify_realtime_setup.py
```

---

## Quick Reference

### In Command Prompt (CMD):
```cmd
cd E:\youssef_anas\game-boosters-main
venv\Scripts\activate.bat
python verify_realtime_setup.py
python manage.py migrate --noinput
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

### In PowerShell (After fixing execution policy):
```powershell
cd E:\youssef_anas\game-boosters-main
venv\Scripts\activate
python verify_realtime_setup.py
python manage.py migrate --noinput
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

### Without Virtual Environment (Simplest):
```powershell
cd E:\youssef_anas\game-boosters-main
python verify_realtime_setup.py
python manage.py migrate --noinput
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Recommended: Use Command Prompt (CMD)

**Easiest solution - just switch to CMD:**

1. Open **Command Prompt** (Win + R, type `cmd`, Enter)
2. Navigate to project: `cd E:\youssef_anas\game-boosters-main`
3. Run commands one by one from the list above

No execution policy issues with CMD!


