"""
Verification script for real-time order sync setup
Checks each step before starting the server
"""
import os
import sys
import subprocess

def check_step(step_num, step_name):
    """Print step header"""
    print(f"\n{'='*60}")
    print(f"Step {step_num}: {step_name}")
    print(f"{'='*60}")

def check_virtual_environment():
    """Check if virtual environment is activated"""
    check_step(1, "Checking Virtual Environment")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ Virtual environment is activated")
        return True
    else:
        print("✗ Virtual environment is NOT activated")
        print("  → Run: venv\\Scripts\\activate (Windows)")
        print("  → Run: source venv/bin/activate (Linux/Mac)")
        return False

def check_django():
    """Check if Django is installed"""
    check_step(2, "Checking Django Installation")
    
    try:
        import django
        print(f"✓ Django is installed (version {django.get_version()})")
        return True
    except ImportError:
        print("✗ Django is NOT installed")
        print("  → Run: pip install -r requirements.txt")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    check_step(3, "Checking Dependencies")
    
    required_packages = {
        'channels': 'channels',
        'channels_redis': 'channels-redis',
        'daphne': 'daphne',
    }
    
    all_installed = True
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is NOT installed")
            print(f"  → Run: pip install {package_name}")
            all_installed = False
    
    return all_installed

def check_database():
    """Check if database is accessible"""
    check_step(4, "Checking Database Connection")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
        import django
        django.setup()
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✓ Database connection is working")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("  → Check your database settings in settings.py")
        print("  → Make sure PostgreSQL is running")
        return False

def check_migrations():
    """Check if migrations need to be applied"""
    check_step(5, "Checking Migrations")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
        import django
        django.setup()
        
        from django.core.management import call_command
        from io import StringIO
        
        # Check for pending migrations
        output = StringIO()
        call_command('showmigrations', '--plan', stdout=output)
        output.seek(0)
        migrations_output = output.read()
        
        if '[ ]' in migrations_output:
            print("⚠️  There are pending migrations")
            print("  → Run: python manage.py migrate --noinput")
            return False
        else:
            print("✓ All migrations are applied")
            return True
    except Exception as e:
        print(f"✗ Error checking migrations: {e}")
        return False

def check_redis():
    """Check if Redis is running"""
    check_step(6, "Checking Redis")
    
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=1)
        r.ping()
        print("✓ Redis is running on localhost:6379")
        return True
    except Exception as e:
        print("⚠️  Redis is NOT running (this is OK for development)")
        print("  → Server will use InMemoryChannelLayer")
        print("  → To start Redis: docker compose up -d redis")
        return False

def check_channel_layer():
    """Check if channel layer is configured"""
    check_step(7, "Checking Channel Layer Configuration")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
        import django
        django.setup()
        
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        
        if channel_layer:
            print(f"✓ Channel layer is configured: {type(channel_layer).__name__}")
            return True
        else:
            print("✗ Channel layer is NOT configured")
            return False
    except Exception as e:
        print(f"⚠️  Error checking channel layer: {e}")
        return False

def check_asgi_application():
    """Check if ASGI application can be imported"""
    check_step(8, "Checking ASGI Application")
    
    try:
        from gameBoosterss.asgi import application
        print("✓ ASGI application can be imported")
        return True
    except Exception as e:
        print(f"✗ ASGI application import failed: {e}")
        print("  → Check gameBoosterss/asgi.py")
        return False

def check_realtime_app():
    """Check if realtime app is properly configured"""
    check_step(9, "Checking Realtime App Configuration")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
        import django
        django.setup()
        
        # Check if app is in INSTALLED_APPS
        from django.conf import settings
        if 'realtime.apps.RealtimeConfig' in settings.INSTALLED_APPS:
            print("✓ Realtime app is in INSTALLED_APPS")
        else:
            print("✗ Realtime app is NOT in INSTALLED_APPS")
            return False
        
        # Check if URLs are configured
        from django.urls import resolve
        try:
            resolve('/realtime/test/')
            print("✓ Realtime URLs are configured")
        except:
            print("⚠️  Realtime URLs may not be configured")
        
        return True
    except Exception as e:
        print(f"✗ Error checking realtime app: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("Real-Time Order Sync Setup Verification")
    print("="*60)
    
    results = []
    
    # Run checks
    results.append(("Virtual Environment", check_virtual_environment()))
    results.append(("Django", check_django()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Database", check_database()))
    results.append(("Migrations", check_migrations()))
    results.append(("Redis", check_redis()))
    results.append(("Channel Layer", check_channel_layer()))
    results.append(("ASGI Application", check_asgi_application()))
    results.append(("Realtime App", check_realtime_app()))
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All checks passed! You can start the server:")
        print("   python manage.py migrate --noinput")
        print("   docker compose up -d redis")
        print("   daphne -b 0.0.0.0 -p 8000 gameBoosterss.asgi:application")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before starting the server.")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    main()


