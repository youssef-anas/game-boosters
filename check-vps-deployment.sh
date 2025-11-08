#!/bin/bash
# Script to verify dashboard and code changes are deployed on VPS

echo "🔍 Checking VPS Deployment Status"
echo "=================================="
echo ""

cat << 'EOF'
# Run these commands on your VPS to verify deployment:

# ============================================
# 1. Check if admin_dashboard app exists
# ============================================
echo "1️⃣ Checking admin_dashboard app..."
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml exec web ls -la /app/admin_dashboard/ 2>/dev/null && echo "✅ admin_dashboard directory exists" || echo "❌ admin_dashboard directory NOT found"

# ============================================
# 2. Check if admin_dashboard is in INSTALLED_APPS
# ============================================
echo ""
echo "2️⃣ Checking INSTALLED_APPS for admin_dashboard..."
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << PYEOF
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
import django
django.setup()

from django.conf import settings
apps = settings.INSTALLED_APPS

if 'admin_dashboard.apps.AdminDashboardConfig' in apps or 'admin_dashboard' in apps:
    print("✅ admin_dashboard is in INSTALLED_APPS")
    for app in apps:
        if 'admin_dashboard' in app.lower():
            print(f"   Found: {app}")
else:
    print("❌ admin_dashboard is NOT in INSTALLED_APPS")
    print("Current INSTALLED_APPS:")
    for app in apps:
        if 'dashboard' in app.lower() or 'admin' in app.lower():
            print(f"   - {app}")
PYEOF

# ============================================
# 3. Check if code fixes are present (utils.py files)
# ============================================
echo ""
echo "3️⃣ Checking code fixes in utils.py files..."

# Check WorldOfWarcraft/utils.py
echo "   Checking WorldOfWarcraft/utils.py..."
docker-compose -f docker-compose.prod.yml exec web grep -A 3 "def get_level_up_price" /app/WorldOfWarcraft/utils.py | head -5

# Check csgo2/utils.py
echo ""
echo "   Checking csgo2/utils.py..."
docker-compose -f docker-compose.prod.yml exec web grep -A 3 "def get_premier_prices" /app/csgo2/utils.py | head -5

# Check csgo2/controller/order_information.py
echo ""
echo "   Checking csgo2/controller/order_information.py..."
docker-compose -f docker-compose.prod.yml exec web grep -A 5 "division_prices_data" /app/csgo2/controller/order_information.py | head -10

# ============================================
# 4. Check migrations status
# ============================================
echo ""
echo "4️⃣ Checking migration status..."
docker-compose -f docker-compose.prod.yml exec web python manage.py showmigrations admin_dashboard 2>/dev/null | head -20

# ============================================
# 5. Test dashboard URL accessibility
# ============================================
echo ""
echo "5️⃣ Testing dashboard endpoints..."
echo "   Testing /admin/ endpoint:"
curl -I http://127.0.0.1:8000/admin/ 2>/dev/null | head -3

echo ""
echo "   Testing /admin/dashboard/ endpoint (if exists):"
curl -I http://127.0.0.1:8000/admin/dashboard/ 2>/dev/null | head -3

# ============================================
# 6. Check if recent fixes are in the code
# ============================================
echo ""
echo "6️⃣ Verifying specific code fixes..."

# Check if WorldOfWarcraft/utils.py has the safe return
echo "   WorldOfWarcraft/utils.py - checking for safe None handling:"
docker-compose -f docker-compose.prod.yml exec web grep -E "(return obj.price if obj else 0|if obj else 0)" /app/WorldOfWarcraft/utils.py && echo "   ✅ Safe None handling found" || echo "   ❌ Safe None handling NOT found"

# Check if csgo2/utils.py has at least 6 elements
echo ""
echo "   csgo2/utils.py - checking for 6+ elements in return:"
docker-compose -f docker-compose.prod.yml exec web grep -E "return \[0, 0, 0, 0, 0, 0\]" /app/csgo2/utils.py && echo "   ✅ Default list with 6 elements found" || echo "   ⚠️  Default list might be different"

# ============================================
# 7. Check Git commit history (if repo is on VPS)
# ============================================
echo ""
echo "7️⃣ Checking Git status (if repo exists)..."
cd /opt/game-boosters
if [ -d .git ]; then
    echo "   Latest commits:"
    git log --oneline -5 2>/dev/null || echo "   (Git not accessible in container)"
else
    echo "   ⚠️  No .git directory found (code might be copied, not cloned)"
fi

# ============================================
# 8. Check container logs for errors
# ============================================
echo ""
echo "8️⃣ Checking recent container logs for errors..."
docker-compose -f docker-compose.prod.yml logs --tail=50 web | grep -iE "(error|exception|traceback|admin_dashboard)" | tail -10 || echo "   No recent errors found"

# ============================================
# 9. Test database connection and models
# ============================================
echo ""
echo "9️⃣ Testing database and models..."
docker-compose -f docker-compose.prod.yml exec web python manage.py shell << PYEOF
from django.apps import apps

# Check if admin_dashboard models are loaded
try:
    admin_dashboard_models = apps.get_app_config('admin_dashboard').get_models()
    print(f"✅ admin_dashboard app loaded with {len(list(admin_dashboard_models))} models")
    for model in admin_dashboard_models:
        print(f"   - {model.__name__}")
except Exception as e:
    print(f"❌ admin_dashboard app not loaded: {e}")

# Check if other apps can access their models
try:
    from csgo2.models import Csgo2PremierPrice
    print("✅ csgo2.models.Csgo2PremierPrice accessible")
except Exception as e:
    print(f"⚠️  csgo2.models issue: {e}")

try:
    from WorldOfWarcraft.models import WowLevelUpPrice
    print("✅ WorldOfWarcraft.models.WowLevelUpPrice accessible")
except Exception as e:
    print(f"⚠️  WorldOfWarcraft.models issue: {e}")
PYEOF

echo ""
echo "=================================="
echo "✅ Verification complete!"
echo ""
echo "Next steps:"
echo "1. If admin_dashboard is missing, pull latest code from GitHub"
echo "2. If INSTALLED_APPS is missing admin_dashboard, update settings.py"
echo "3. If migrations are pending, run: docker-compose exec web python manage.py migrate"
echo "4. Access dashboard at: http://46.202.131.43/admin/"

EOF

