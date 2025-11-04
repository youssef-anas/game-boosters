# 🔧 Fix Instructions - Step by Step

## Problem Summary

The verification shows:
- ✗ Virtual environment is NOT activated
- ✗ Django is NOT installed
- ✗ Dependencies are NOT installed

## Solution: Complete Setup

### Option 1: Use the Setup Script (Easiest!)

**Just run:**
```powershell
.\setup_and_start.bat
```

This script will:
1. ✅ Activate/create virtual environment
2. ✅ Upgrade pip
3. ✅ Install all dependencies
4. ✅ Apply migrations
5. ✅ Start Redis (optional)
6. ✅ Start Daphne server

---

### Option 2: Manual Setup (Step by Step)

**Copy and paste these commands one by one:**

#### Step 1: Activate Virtual Environment
```powershell
venv\Scripts\activate
```

**You should see `(venv)` in your prompt:**
```
(venv) PS E:\youssef_anas\game-boosters-main>
```

#### Step 2: Upgrade pip
```powershell
python -m pip install --upgrade pip
```

#### Step 3: Install All Dependencies
```powershell
pip install -r requirements.txt
```

**This will install:**
- Django
- channels
- channels-redis
- daphne
- And all other required packages

**Note:** This may take 5-10 minutes depending on your internet speed.

#### Step 4: Verify Installation
```powershell
python verify_realtime_setup.py
```

**You should now see:**
- ✓ Virtual environment
- ✓ Django
- ✓ Dependencies
- And other checks passing

#### Step 5: Apply Migrations
```powershell
python manage.py migrate --noinput
```

#### Step 6: (Optional) Start Redis
```powershell
docker compose up -d redis
```

**Note:** If Redis is not running, the server will use InMemoryChannelLayer automatically.

#### Step 7: Start Daphne Server
```powershell
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Complete Commands (Copy & Paste)

Run these commands **in order** in PowerShell:

```powershell
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Upgrade pip
python -m pip install --upgrade pip

# 3. Install dependencies (this takes time)
pip install -r requirements.txt

# 4. Verify setup
python verify_realtime_setup.py

# 5. Apply migrations
python manage.py migrate --noinput

# 6. (Optional) Start Redis
docker compose up -d redis

# 7. Start server
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

---

## Expected Output

### After Step 3 (Installing dependencies):
```
Collecting django==5.0.10
  Downloading Django-5.0.10-py3-none-any.whl
Collecting channels==4.1.0
  Downloading channels-4.1.0-py3-none-any.whl
...
Successfully installed django-5.0.10 channels-4.1.0 ...
```

### After Step 4 (Verification):
```
✓ Virtual environment is activated
✓ Django is installed (version 5.0.10)
✓ channels is installed
✓ channels-redis is installed
✓ daphne is installed
...
```

### After Step 7 (Starting server):
```
2024-XX-XX XX:XX:XX [INFO] Starting server at tcp:port=8000:interface=0.0.0.0
2024-XX-XX XX:XX:XX [INFO] Listening on TCP address 0.0.0.0:8000
```

---

## Troubleshooting

### If "venv\Scripts\activate" doesn't work:
```powershell
# Check if venv exists
dir venv

# If not, create it
python -m venv venv

# Then activate
venv\Scripts\activate
```

### If "pip install -r requirements.txt" fails:
```powershell
# Try installing without cache
pip install --no-cache-dir -r requirements.txt

# Or install key packages individually
pip install django==5.0.10
pip install channels==4.1.0
pip install channels-redis==4.1.0
pip install daphne==4.1.2
```

### If installation takes too long:
- This is normal! Installing all dependencies can take 5-10 minutes
- Be patient and wait for it to complete
- Make sure you have internet connection

### If you get permission errors:
- Run PowerShell as Administrator
- Or try: `python -m pip install --user -r requirements.txt`

---

## After Setup

Once everything is installed:

1. **Run verification:**
   ```powershell
   python verify_realtime_setup.py
   ```
   Should show 9/9 checks passed

2. **Start the server:**
   ```powershell
   daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
   ```

3. **Access test page:**
   - http://localhost:8000/realtime/test/

---

## Quick Summary

**The problem:** Virtual environment not activated, so Python can't find Django and dependencies.

**The solution:** Activate virtual environment, then install dependencies.

**The easiest way:** Run `.\setup_and_start.bat` - it does everything automatically!


