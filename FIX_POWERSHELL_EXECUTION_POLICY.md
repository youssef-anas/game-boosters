# 🔧 Fix: PowerShell Execution Policy Error

## Problem

PowerShell is blocking script execution with this error:
```
File cannot be loaded because running scripts is disabled on this system
```

## Solutions

### Solution 1: Use Command Prompt (CMD) Instead (Easiest!)

**Switch to CMD instead of PowerShell:**

1. Open **Command Prompt** (not PowerShell)
2. Navigate to your project:
   ```cmd
   cd E:\youssef_anas\game-boosters-main
   ```
3. Activate virtual environment:
   ```cmd
   venv\Scripts\activate.bat
   ```

**This should work without any policy issues!**

---

### Solution 2: Fix PowerShell Execution Policy (One-time Setup)

**Run PowerShell as Administrator, then:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Then try activating again:**
```powershell
venv\Scripts\activate
```

---

### Solution 3: Bypass for Current Session Only

**Run this command in PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

**Then activate:**
```powershell
venv\Scripts\activate
```

**Note:** This only works for the current PowerShell session.

---

### Solution 4: Use activate.bat Directly

**Instead of `activate`, use:**
```powershell
venv\Scripts\activate.bat
```

**Or:**
```powershell
cmd /c venv\Scripts\activate.bat
```

---

## Recommended: Use CMD

**The easiest solution is to use Command Prompt (CMD) instead of PowerShell:**

1. Open **Command Prompt** (Win + R, type `cmd`, press Enter)
2. Navigate to project:
   ```cmd
   cd E:\youssef_anas\game-boosters-main
   ```
3. Activate venv:
   ```cmd
   venv\Scripts\activate.bat
   ```

**You should see `(venv)` in your prompt!**


