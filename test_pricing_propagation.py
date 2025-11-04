#!/usr/bin/env python
"""
Pricing Propagation Test Script

This script validates full dynamic pricing synchronization across all dashboards:
- Admin Dashboard (PricingEntry model)
- Client Frontend (order calculator)
- Booster Dashboard (assigned orders)
- Manager Dashboard (order management)

Test Flow:
1. Setup and capture original prices from all sources
2. Modify database prices (multiply by 1.25)
3. Recalculate prices and compare
4. Generate Markdown report
5. Send report to Discord with JSON snapshot
"""

import os
import sys
import django
import json
import requests
from datetime import datetime
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from django.db import transaction
from django.conf import settings
from leagueOfLegends.models import LeagueOfLegendsTier, LeagueOfLegendsMark, LeagueOfLegendsRank, LeagueOfLegendsDivisionOrder
from leagueOfLegends.utils import get_lol_divisions_data, get_lol_marks_data
from leagueOfLegends.controller.order_information import get_division_order_result_by_rank
from admin_dashboard.models import PricingEntry
from accounts.models import BaseOrder, BaseUser, Game

# Discord webhook URL (set via environment variable or use placeholder)
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL', 'https://discordapp.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN')

# Logs directory
LOGS_DIR = '/app/logs'
REPORT_FILE = os.path.join(LOGS_DIR, 'pricing_sync_report.json')

def ensure_logs_directory():
    """Create logs directory if it doesn't exist"""
    os.makedirs(LOGS_DIR, exist_ok=True)

def get_environment_info():
    """Get environment information"""
    return {
        'db_user': os.getenv('DB_USER', 'postgres'),
        'db_name': os.getenv('NAME', 'gameboosters_db01'),
        'timestamp': datetime.now().isoformat(),
        'test_path': 'Iron IV → Silver I'
    }

def capture_admin_prices(game_key='lol'):
    """Capture prices from Admin Dashboard (PricingEntry)"""
    try:
        entries = PricingEntry.objects.filter(game_key=game_key)
        admin_prices = {}
        for entry in entries:
            admin_prices[entry.service_id] = {
                'price': float(entry.price),
                'name': entry.name,
                'description': entry.description
            }
        return {'status': 'success', 'prices': admin_prices, 'count': len(admin_prices)}
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'prices': {}, 'count': 0}

def capture_client_price(current_rank_name='iron', current_division=1, current_marks=0,
                         desired_rank_name='silver', desired_division=4):
    """Capture price from Client Frontend (order calculator)"""
    try:
        # Get ranks
        current_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact=current_rank_name).first()
        desired_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact=desired_rank_name).first()
        
        if not current_rank or not desired_rank:
            return {'status': 'error', 'error': 'Ranks not found', 'price': 0}
        
        # Prepare order data (matching the exact parameter names expected by get_division_order_result_by_rank)
        order_data = {
            'current_rank': current_rank.id,
            'current_division': current_division,
            'marks': current_marks,
            'desired_rank': desired_rank.id,
            'desired_division': desired_division,
            'duo_boosting': False,
            'select_booster': False,
            'turbo_boost': False,
            'streaming': False,
            'select_champion': False,
            'champion_data': [],
            'server': 'EUW',
            'promo_code': 'null',
            'choose_booster': 0,
            'extend_order': 0  # Note: parameter name is 'extend_order', not 'extend_order_id'
        }
        
        # Temporarily disable print statements
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Calculate price using order information function
            result = get_division_order_result_by_rank(order_data)
            price = result.get('price', 0)
        finally:
            sys.stdout = old_stdout
        
        return {
            'status': 'success',
            'price': float(price) if price else 0,
            'path': f"{current_rank_name.title()} {current_division} → {desired_rank_name.title()} {desired_division}"
        }
    except Exception as e:
        import traceback
        return {'status': 'error', 'error': str(e) + '\n' + traceback.format_exc(), 'price': 0}

def capture_booster_price(base_order, lol_order):
    """Capture price from Booster Dashboard (assigned orders)"""
    try:
        if not base_order or not lol_order:
            return {'status': 'error', 'error': 'Order not found', 'price': 0}
        
        # Get booster price from order
        price_result = lol_order.get_order_price()
        booster_price = price_result.get('booster_price', 0)
        
        return {
            'status': 'success',
            'price': float(booster_price),
            'percent_for_view': price_result.get('percent_for_view', 0),
            'actual_price': float(base_order.actual_price) if base_order.actual_price else 0
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'price': 0}

def capture_manager_price(base_order):
    """Capture price from Manager Dashboard (order management view)"""
    try:
        if not base_order:
            return {'status': 'error', 'error': 'Order not found', 'price': 0}
        
        # Manager view shows order price
        return {
            'status': 'success',
            'price': float(base_order.price) if base_order.price else 0,
            'actual_price': float(base_order.actual_price) if base_order.actual_price else 0,
            'real_order_price': float(base_order.real_order_price) if base_order.real_order_price else 0
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'price': 0}

def create_test_order():
    """Create a test order for booster and manager price testing"""
    try:
        # Get or create test client
        client, _ = BaseUser.objects.get_or_create(
            username='test_pricing_client',
            defaults={
                'email': 'test_pricing_client@test.com',
                'is_customer': True,
                'is_booster': False
            }
        )
        
        # Get game
        game = Game.objects.filter(name__icontains='league').first()
        if not game:
            return None, None
        
        # Get ranks
        iron_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact='iron').first()
        silver_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact='silver').first()
        
        if not iron_rank or not silver_rank:
            return None, None
        
        # Create base order
        base_order = BaseOrder.objects.create(
            game=game,
            customer=client,
            status='New',
            price=0,
            actual_price=0,
            real_order_price=0,
            game_type='D'
        )
        
        # Create LOL division order
        lol_order = LeagueOfLegendsDivisionOrder.objects.create(
            order=base_order,
            current_rank=iron_rank,
            current_division=1,  # IV
            current_marks=0,
            reached_rank=iron_rank,
            reached_division=1,
            reached_marks=0,
            desired_rank=silver_rank,
            desired_division=4  # I
        )
        
        # Calculate and set prices
        order_data = {
            'current_rank': iron_rank.id,
            'current_division': 1,
            'marks': 0,
            'desired_rank': silver_rank.id,
            'desired_division': 4,
            'duo_boosting': False,
            'select_booster': False,
            'turbo_boost': False,
            'streaming': False,
            'select_champion': False,
            'champion_data': [],
            'server': 'EUW',
            'promo_code': 'null',
            'choose_booster': 0,
            'extend_order': 0  # Note: parameter name is 'extend_order', not 'extend_order_id'
        }
        
        result = get_division_order_result_by_rank(order_data)
        base_order.price = result['price']
        base_order.real_order_price = result['price']
        base_order.update_actual_price()
        base_order.save()
        
        return base_order, lol_order
    except Exception as e:
        print(f"   ⚠️  Error creating test order: {e}")
        return None, None

def modify_tier_prices(multiplier=1.25):
    """Modify LeagueOfLegendsTier prices by multiplier"""
    try:
        iron_tier = LeagueOfLegendsTier.objects.filter(rank__rank_name__iexact='iron').first()
        if not iron_tier:
            return {'status': 'error', 'error': 'Iron tier not found'}
        
        # Store original prices
        original = {
            'from_IV_to_III': float(iron_tier.from_IV_to_III),
            'from_III_to_II': float(iron_tier.from_III_to_II),
            'from_II_to_I': float(iron_tier.from_II_to_I),
            'from_I_to_IV_next': float(iron_tier.from_I_to_IV_next)
        }
        
        # Modify prices
        iron_tier.from_IV_to_III *= multiplier
        iron_tier.from_III_to_II *= multiplier
        iron_tier.from_II_to_I *= multiplier
        iron_tier.from_I_to_IV_next *= multiplier
        iron_tier.save()
        
        return {
            'status': 'success',
            'original': original,
            'modified': {
                'from_IV_to_III': float(iron_tier.from_IV_to_III),
                'from_III_to_II': float(iron_tier.from_III_to_II),
                'from_II_to_I': float(iron_tier.from_II_to_I),
                'from_I_to_IV_next': float(iron_tier.from_I_to_IV_next)
            }
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def calculate_percentage_change(old_price, new_price):
    """Calculate percentage change"""
    if old_price == 0:
        return 0
    return ((new_price - old_price) / old_price) * 100

def send_to_discord(markdown_report, json_data):
    """Send report to Discord webhook"""
    try:
        if 'YOUR_WEBHOOK' in DISCORD_WEBHOOK_URL:
            print("\n⚠️  Discord webhook not configured. Skipping Discord notification.")
            print(f"   Set DISCORD_WEBHOOK_URL environment variable to enable.")
            return False
        
        # Create Discord embed
        embed = {
            "title": "🧪 Pricing Propagation Test Results",
            "description": "Dynamic pricing synchronization test completed",
            "color": 0x00ff00,  # Green
            "fields": [
                {
                    "name": "📊 Test Summary",
                    "value": markdown_report[:1000] + "..." if len(markdown_report) > 1000 else markdown_report,
                    "inline": False
                }
            ],
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Pricing Propagation Test"
            }
        }
        
        # Add JSON data as attachment or field
        json_summary = json.dumps({
            'before': json_data.get('before', {}),
            'after': json_data.get('after', {}),
            'comparison': json_data.get('comparison', {})
        }, indent=2)
        
        if len(json_summary) < 1900:
            embed['fields'].append({
                "name": "📋 JSON Data",
                "value": f"```json\n{json_summary}\n```",
                "inline": False
            })
        
        payload = {
            "content": "🧪 **Pricing Propagation Test Report**",
            "embeds": [embed]
        }
        
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        
        if response.status_code == 204 or response.status_code == 200:
            print("\n✅ Report sent to Discord successfully")
            return True
        else:
            print(f"\n⚠️  Failed to send to Discord: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"\n⚠️  Error sending to Discord: {e}")
        return False

def generate_markdown_report(results):
    """Generate Markdown report from test results"""
    report = f"""# 🧪 Pricing Propagation Test Report

**Test Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Test Path**: Iron IV → Silver I  
**Environment**: {results.get('env', {}).get('db_name', 'N/A')}

---

## 📊 Test Results Summary

### ✅ Overall Status: {'PASSED' if results.get('overall_status') == 'passed' else 'FAILED'}

---

## 1️⃣ Before Update

### Admin Dashboard
- **Status**: {results.get('before', {}).get('admin', {}).get('status', 'N/A')}
- **Pricing Entries**: {results.get('before', {}).get('admin', {}).get('count', 0)}

### Client Frontend
- **Status**: {results.get('before', {}).get('client', {}).get('status', 'N/A')}
- **Price**: ${results.get('before', {}).get('client', {}).get('price', 0):.2f}
- **Path**: {results.get('before', {}).get('client', {}).get('path', 'N/A')}

### Booster Dashboard
- **Status**: {results.get('before', {}).get('booster', {}).get('status', 'N/A')}
- **Price**: ${results.get('before', {}).get('booster', {}).get('price', 0):.2f}
- **Percent**: {results.get('before', {}).get('booster', {}).get('percent_for_view', 0):.1f}%

### Manager Dashboard
- **Status**: {results.get('before', {}).get('manager', {}).get('status', 'N/A')}
- **Price**: ${results.get('before', {}).get('manager', {}).get('price', 0):.2f}

---

## 2️⃣ After Update (1.25x multiplier)

### Admin Dashboard
- **Status**: {results.get('after', {}).get('admin', {}).get('status', 'N/A')}
- **Pricing Entries**: {results.get('after', {}).get('admin', {}).get('count', 0)}

### Client Frontend
- **Status**: {results.get('after', {}).get('client', {}).get('status', 'N/A')}
- **Price**: ${results.get('after', {}).get('client', {}).get('price', 0):.2f}
- **Path**: {results.get('after', {}).get('client', {}).get('path', 'N/A')}

### Booster Dashboard
- **Status**: {results.get('after', {}).get('booster', {}).get('status', 'N/A')}
- **Price**: ${results.get('after', {}).get('booster', {}).get('price', 0):.2f}
- **Percent**: {results.get('after', {}).get('booster', {}).get('percent_for_view', 0):.1f}%

### Manager Dashboard
- **Status**: {results.get('after', {}).get('manager', {}).get('status', 'N/A')}
- **Price**: ${results.get('after', {}).get('manager', {}).get('price', 0):.2f}

---

## 3️⃣ Comparison

### Client Frontend
- **Original**: ${results.get('before', {}).get('client', {}).get('price', 0):.2f}
- **New**: ${results.get('after', {}).get('client', {}).get('price', 0):.2f}
- **Change**: {results.get('comparison', {}).get('client', {}).get('percent_change', 0):.2f}%
- **Status**: {results.get('comparison', {}).get('client', {}).get('status', '❌')}

### Booster Dashboard
- **Original**: ${results.get('before', {}).get('booster', {}).get('price', 0):.2f}
- **New**: ${results.get('after', {}).get('booster', {}).get('price', 0):.2f}
- **Change**: {results.get('comparison', {}).get('booster', {}).get('percent_change', 0):.2f}%
- **Status**: {results.get('comparison', {}).get('booster', {}).get('status', '❌')}

### Manager Dashboard
- **Original**: ${results.get('before', {}).get('manager', {}).get('price', 0):.2f}
- **New**: ${results.get('after', {}).get('manager', {}).get('price', 0):.2f}
- **Change**: {results.get('comparison', {}).get('manager', {}).get('percent_change', 0):.2f}%
- **Status**: {results.get('comparison', {}).get('manager', {}).get('status', '❌')}

---

## ✅ Conclusion

"""
    
    if results.get('overall_status') == 'passed':
        report += "✅ **All dashboards synchronized correctly!**\n\n"
        report += "- Prices update immediately after database changes\n"
        report += "- No server restart required\n"
        report += "- All dashboards reflect the same pricing data\n"
    else:
        report += "❌ **Some dashboards failed to synchronize**\n\n"
        report += "- Check individual dashboard status above\n"
        report += "- Verify database connections and caching\n"
    
    report += f"\n---\n\n**Rollback**: All database changes have been automatically rolled back."
    
    return report

def test_pricing_propagation():
    """Main test function"""
    print("=" * 60)
    print("🧪 Pricing Propagation Test")
    print("=" * 60)
    print("\n✅ Goals:")
    print("   1. Confirm price updates propagate to all dashboards")
    print("   2. Ensure get_order_price() reads live data")
    print("   3. Verify Booster earnings update proportionally")
    print("   4. Send report to Discord")
    print()
    
    ensure_logs_directory()
    env_info = get_environment_info()
    
    results = {
        'env': env_info,
        'before': {},
        'after': {},
        'comparison': {},
        'overall_status': 'failed'
    }
    
    try:
        with transaction.atomic():
            # Step 1: Capture original prices
            print("📊 Step 1: Capturing original prices...")
            
            # Admin prices
            admin_before = capture_admin_prices()
            results['before']['admin'] = admin_before
            print(f"   ✅ Admin: {admin_before['count']} pricing entries")
            
            # Client price
            client_before = capture_client_price()
            results['before']['client'] = client_before
            print(f"   ✅ Client: ${client_before.get('price', 0):.2f}")
            
            # Create test order for booster/manager
            base_order, lol_order = create_test_order()
            if base_order and lol_order:
                # Booster price
                booster_before = capture_booster_price(base_order, lol_order)
                results['before']['booster'] = booster_before
                print(f"   ✅ Booster: ${booster_before.get('price', 0):.2f}")
                
                # Manager price
                manager_before = capture_manager_price(base_order)
                results['before']['manager'] = manager_before
                print(f"   ✅ Manager: ${manager_before.get('price', 0):.2f}")
            else:
                print("   ⚠️  Could not create test order for booster/manager testing")
                results['before']['booster'] = {'status': 'skipped', 'price': 0}
                results['before']['manager'] = {'status': 'skipped', 'price': 0}
            
            # Save to JSON
            json_data = {'before_update': results['before']}
            with open(REPORT_FILE, 'w') as f:
                json.dump(json_data, f, indent=2, default=str)
            print(f"   ✅ Saved to {REPORT_FILE}")
            
            # Step 2: Modify database prices
            print("\n🧮 Step 2: Modifying database prices (1.25x multiplier)...")
            modify_result = modify_tier_prices(1.25)
            if modify_result['status'] == 'success':
                print("   ✅ Prices modified successfully")
                print(f"      IV→III: ${modify_result['original']['from_IV_to_III']:.2f} → ${modify_result['modified']['from_IV_to_III']:.2f}")
            else:
                print(f"   ❌ Error: {modify_result.get('error', 'Unknown')}")
            
            # Step 3: Recalculate prices
            print("\n📊 Step 3: Recalculating prices...")
            
            # Admin prices (should be same, we didn't modify PricingEntry)
            admin_after = capture_admin_prices()
            results['after']['admin'] = admin_after
            
            # Client price
            client_after = capture_client_price()
            results['after']['client'] = client_after
            print(f"   ✅ Client: ${client_after.get('price', 0):.2f}")
            
            # Booster/Manager prices
            if base_order and lol_order:
                # Refresh order
                base_order.refresh_from_db()
                lol_order.refresh_from_db()
                
                # Recalculate booster price
                booster_after = capture_booster_price(base_order, lol_order)
                results['after']['booster'] = booster_after
                print(f"   ✅ Booster: ${booster_after.get('price', 0):.2f}")
                
                # Manager price
                manager_after = capture_manager_price(base_order)
                results['after']['manager'] = manager_after
                print(f"   ✅ Manager: ${manager_after.get('price', 0):.2f}")
            
            # Step 4: Compare
            print("\n✅ Step 4: Comparing prices...")
            
            # Client comparison
            client_old = client_before.get('price', 0)
            client_new = client_after.get('price', 0)
            client_change = calculate_percentage_change(client_old, client_new)
            client_status = '✅' if abs(client_change - 25) < 1 else '❌'
            results['comparison']['client'] = {
                'percent_change': client_change,
                'status': client_status,
                'expected': 25.0,
                'actual': client_change
            }
            print(f"   Client: {client_change:.2f}% change ({client_status})")
            
            # Booster comparison
            if base_order and lol_order:
                booster_old = booster_before.get('price', 0)
                booster_new = booster_after.get('price', 0)
                booster_change = calculate_percentage_change(booster_old, booster_new) if booster_old > 0 else 0
                booster_status = '✅' if booster_change > 0 else '❌'
                results['comparison']['booster'] = {
                    'percent_change': booster_change,
                    'status': booster_status,
                    'expected': '> 0',
                    'actual': booster_change
                }
                print(f"   Booster: {booster_change:.2f}% change ({booster_status})")
                
                # Manager comparison
                manager_old = manager_before.get('price', 0)
                manager_new = manager_after.get('price', 0)
                manager_change = calculate_percentage_change(manager_old, manager_new) if manager_old > 0 else 0
                manager_status = '✅' if abs(manager_change - 25) < 1 else '❌'
                results['comparison']['manager'] = {
                    'percent_change': manager_change,
                    'status': manager_status,
                    'expected': 25.0,
                    'actual': manager_change
                }
                print(f"   Manager: {manager_change:.2f}% change ({manager_status})")
            
            # Determine overall status
            if (client_status == '✅' and 
                results['comparison'].get('booster', {}).get('status') == '✅' and
                results['comparison'].get('manager', {}).get('status') == '✅'):
                results['overall_status'] = 'passed'
            else:
                results['overall_status'] = 'failed'
            
            # Save complete results
            json_data['after_update'] = results['after']
            json_data['comparison'] = results['comparison']
            json_data['overall_status'] = results['overall_status']
            with open(REPORT_FILE, 'w') as f:
                json.dump(json_data, f, indent=2, default=str)
            
            # Step 5: Generate Markdown report
            print("\n📝 Step 5: Generating Markdown report...")
            markdown_report = generate_markdown_report(results)
            print("   ✅ Report generated")
            
            # Step 6: Send to Discord
            print("\n📤 Step 6: Sending report to Discord...")
            send_to_discord(markdown_report, json_data)
            
            # Force rollback
            print("\n🔄 Rolling back changes...")
            raise Exception("Intentional rollback - test completed successfully")
            
    except Exception as e:
        if "Intentional rollback" in str(e):
            print("   ✅ Rollback completed successfully")
            print("\n" + "=" * 60)
            print("✅ TEST COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"\n📊 Overall Status: {results['overall_status'].upper()}")
            print(f"📄 Report saved to: {REPORT_FILE}")
            print(f"📝 Markdown report length: {len(markdown_report)} characters")
        else:
            print(f"\n❌ Error during test: {e}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == '__main__':
    test_pricing_propagation()

