# Activating Virtual Environment

## Issue: ModuleNotFoundError: No module named 'django'

This means the virtual environment is not activated.

## Solution: Activate Virtual Environment

### On Windows (PowerShell or CMD):

**Option 1: Using the batch script (recommended)**
```bash
start_realtime_server_full.bat
```
This script will automatically activate the virtual environment for you.

**Option 2: Manual activation**
```bash
# Navigate to project directory
cd E:\youssef_anas\game-boosters-main

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your prompt
# Now run commands
python manage.py migrate --noinput
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

### On Linux/Mac:

```bash
# Navigate to project directory
cd /path/to/game-boosters-main

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
# Now run commands
python manage.py migrate --noinput
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

## Verify Virtual Environment is Activated

After activation, you should see `(venv)` at the start of your command prompt:

```
(venv) PS E:\youssef_anas\game-boosters-main>
```

## If Virtual Environment Doesn't Exist

If the `venv` folder doesn't exist, create it:

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### On Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Quick Start Commands

Once virtual environment is activated:

```bash
# 1. Apply migrations
python manage.py migrate --noinput

# 2. Start Redis (optional)
docker compose up -d redis

# 3. Start Daphne
daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application
```

## Using the Batch Script

The easiest way is to use the provided batch script:

```bash
start_realtime_server_full.bat
```

This will:
1. Automatically activate the virtual environment
2. Apply migrations
3. Start Redis (if using Docker)
4. Start Daphne server



