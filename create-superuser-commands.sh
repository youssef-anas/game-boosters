#!/bin/bash
# Commands to create or reset Django superuser

echo "🔐 Creating Django Superuser"
echo ""
echo "Run these commands on your VPS:"

cat << 'EOF'
# ============================================
# OPTION 1: Create a new superuser interactively
# ============================================
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# You will be prompted to enter:
# - Username
# - Email address (optional)
# - Password (twice for confirmation)

# ============================================
# OPTION 2: Create superuser non-interactively
# ============================================
# Set these variables with your desired values:
USERNAME="admin"
EMAIL="admin@madboost.gg"
PASSWORD="YourSecurePassword123!"

# Create superuser (will fail if user already exists)
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << PYTHON_EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "$USERNAME"
email = "$EMAIL"
password = "$PASSWORD"

if User.objects.filter(username=username).exists():
    print(f"❌ User '{username}' already exists!")
    print("Use OPTION 3 to reset password instead.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created successfully!")
PYTHON_EOF

# ============================================
# OPTION 3: Reset password for existing user
# ============================================
# First, check existing users:
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << PYTHON_EOF
from django.contrib.auth import get_user_model
User = get_user_model()

print("Existing superusers:")
for user in User.objects.filter(is_superuser=True):
    print(f"  - Username: {user.username}, Email: {user.email}")
PYTHON_EOF

# Then reset password for a specific user:
USERNAME="admin"  # Change to your username
NEW_PASSWORD="YourNewPassword123!"

docker-compose -f docker-compose.prod.yml exec web python manage.py shell << PYTHON_EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = "$USERNAME"
new_password = "$NEW_PASSWORD"

try:
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()
    print(f"✅ Password reset for user '{username}'")
except User.DoesNotExist:
    print(f"❌ User '{username}' not found!")
PYTHON_EOF

# ============================================
# OPTION 4: List all users
# ============================================
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << PYTHON_EOF
from django.contrib.auth import get_user_model
User = get_user_model()

print("All users:")
for user in User.objects.all():
    print(f"  - Username: {user.username}, Email: {user.email}, Superuser: {user.is_superuser}")
PYTHON_EOF

EOF

