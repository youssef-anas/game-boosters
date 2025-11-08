# 🔐 How to Create Admin Account

## 📍 Method 1: Interactive Creation (Recommended)

### Step 1: SSH into your VPS
```bash
ssh -i /c/Users/youss/.ssh/id_rsa root@46.202.131.43
```

### Step 2: Navigate to project directory
```bash
cd /opt/game-boosters
```

### Step 3: Create superuser interactively
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

**You will be prompted to enter:**
- **Username**: `admin` (or your choice)
- **Email address**: `admin@madboost.gg` (optional, can leave blank)
- **Password**: Enter a strong password (twice for confirmation)

**Example:**
```
Username: admin
Email address: admin@madboost.gg
Password: ********
Password (again): ********
Superuser created successfully.
```

---

## 📍 Method 2: Non-Interactive (One-Liner)

### Quick Command
```bash
cd /opt/game-boosters && docker-compose -f docker-compose.prod.yml exec web python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()

username = "admin"
email = "admin@madboost.gg"
password = "Admin123!"

if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"✅ Password reset for existing user '{username}'")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created successfully!")
PYEOF
```

**This will:**
- Create a superuser with username `admin` and password `Admin123!`
- Or reset the password if the user already exists

---

## 📍 Method 3: Using Python Shell Directly

### Step 1: Access Python shell
```bash
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
```

### Step 2: In the Python shell, run:
```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Create superuser
username = "admin"
email = "admin@madboost.gg"
password = "YourSecurePassword123!"

User.objects.create_superuser(
    username=username,
    email=email,
    password=password
)

print(f"✅ Superuser '{username}' created successfully!")
exit()
```

---

## 📍 Method 4: Check Existing Users First

### Step 1: Check if admin user exists
```bash
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()

print("Existing superusers:")
for user in User.objects.filter(is_superuser=True):
    print(f"  - Username: {user.username}")
    print(f"  - Email: {user.email}")
    print(f"  - Is Staff: {user.is_staff}")
    print(f"  ---")
PYEOF
```

### Step 2: If user exists, reset password
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()

username = "admin"  # Change to the username you found
new_password = "YourNewPassword123!"

try:
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"✅ Password reset for user '{username}'")
    print(f"   New password: {new_password}")
except User.DoesNotExist:
    print(f"❌ User '{username}' not found!")
PYEOF
```

---

## ✅ Verify Admin Account

### Test Login
1. **Open browser**: Go to `http://46.202.131.43/admin/`
2. **Enter credentials**:
   - Username: `admin` (or your chosen username)
   - Password: `Admin123!` (or your chosen password)
3. **Click "Log in"**

### Verify Access
- You should see the Django admin interface
- You should be able to access `/admin/dashboard/`
- You should see all models in the admin panel

---

## 🔧 Troubleshooting

### Issue 1: "Command not found"
**Solution**: Make sure you're in the project directory and Docker containers are running:
```bash
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml ps
```

### Issue 2: "Container not running"
**Solution**: Start the containers:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Issue 3: "User already exists"
**Solution**: Use Method 4 to check existing users, then reset password

### Issue 4: "Cannot connect to database"
**Solution**: Check if database container is healthy:
```bash
docker-compose -f docker-compose.prod.yml ps db
```

---

## 📝 Recommended Credentials

For production, use strong credentials:
- **Username**: `admin` or your choice
- **Email**: `admin@madboost.gg`
- **Password**: At least 12 characters, mix of letters, numbers, and symbols

**Example strong password**: `MadBoost2024!Admin`

---

## 🎯 Quick Reference

**Most Common Command:**
```bash
cd /opt/game-boosters && docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

**One-Liner (Create or Reset):**
```bash
cd /opt/game-boosters && docker-compose -f docker-compose.prod.yml exec web python manage.py shell << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()
username = "admin"
email = "admin@madboost.gg"
password = "Admin123!"
if User.objects.filter(username=username).exists():
    User.objects.get(username=username).set_password(password)
    print("✅ Password reset")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created")
PYEOF
```

---

**Last Updated**: November 2024

