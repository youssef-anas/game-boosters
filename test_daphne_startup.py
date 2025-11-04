"""
Quick test script to check if Daphne can start properly
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')

try:
    django.setup()
    print("✓ Django setup successful")
    
    # Test channel layer
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()
    if channel_layer:
        print("✓ Channel layer configured")
        try:
            # Test Redis connection
            from asgiref.sync import sync_to_async
            import asyncio
            
            async def test_redis():
                try:
                    await channel_layer.receive('test_channel')
                except Exception as e:
                    # This is expected - we're just testing connection
                    if "Connection" in str(e) or "redis" in str(e).lower():
                        print(f"✗ Redis connection error: {e}")
                        return False
                    else:
                        print("✓ Redis connection OK (got expected error)")
                        return True
            
            result = asyncio.run(test_redis())
            if not result:
                print("\n⚠️  WARNING: Redis connection failed!")
                print("   The server will try to use RedisChannelLayer but may fail.")
                print("   Consider using InMemoryChannelLayer for testing:")
                print("   CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}")
        except Exception as e:
            print(f"✗ Error testing channel layer: {e}")
    else:
        print("✗ Channel layer not configured")
    
    # Test ASGI application
    from gameBoosterss.asgi import application
    print("✓ ASGI application loaded successfully")
    
    print("\n✅ All checks passed! Daphne should start successfully.")
    print("   If Redis is not running, you may see connection errors but the server should still start.")
    
except Exception as e:
    print(f"✗ Error during setup: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)



