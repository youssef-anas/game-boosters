#!/usr/bin/env python
"""
Test League of Legends pricing using realistic order creation flow
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from leagueOfLegends.controller.order_information import get_division_order_result_by_rank
from customer.controllers.order_creator import create_order
from accounts.models import BaseUser, BaseOrder, Captcha
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsRank
from games.models import Game
from admin_dashboard.models import PricingEntry
import random

def get_or_create_test_client():
    """Get or create a test client"""
    client, created = BaseUser.objects.get_or_create(
        username='test_client_realistic',
        defaults={
            'email': 'test_client_realistic@test.com',
            'is_customer': True,
            'is_active': True
        }
    )
    if created:
        client.set_password('test123')
        client.save()
    return client

def get_rank_by_name(rank_name):
    """Get rank by name (case-insensitive)"""
    rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact=rank_name).first()
    if not rank:
        raise ValueError(f"Rank '{rank_name}' not found in database")
    return rank

def create_realistic_order(client, current_rank, current_division, current_marks,
                          desired_rank, desired_division, test_case_name):
    """Create a realistic order using the normal order creation flow"""
    try:
        print(f"\n{'='*60}")
        print(f"Creating order: {test_case_name}")
        print(f"{'='*60}")
        
        # Step 1: Prepare order data (as if coming from frontend)
        order_data = {
            'current_rank': current_rank.pk,
            'current_division': current_division,
            'marks': current_marks,
            'desired_rank': desired_rank.pk,
            'desired_division': desired_division,
            'duo_boosting': False,
            'select_booster': False,
            'turbo_boost': False,
            'streaming': False,
            'select_champion': False,
            'server': 'EUW',
            'price': 0,  # Will be calculated
            'choose_booster': 0,
            'champion_data': '',
            'extend_order': 0,
            'promo_code': 'null'
        }
        
        # Step 2: Calculate price using the order creation logic
        print("\n💰 Calculating price using order creation logic...")
        order_info = get_division_order_result_by_rank(order_data)
        calculated_price = order_info['price']
        invoice = order_info['invoice']
        name = order_info['name']
        
        # Truncate name to 30 characters (BaseOrder.name max_length=30)
        if len(name) > 30:
            name = name[:27] + "..."
        
        print(f"   Calculated Price: ${calculated_price:.2f}")
        print(f"   Order Name: {name} (truncated to 30 chars)")
        print(f"   Invoice: {invoice[:50]}...")
        
        # Step 3: Create a captcha for the order
        captcha = Captcha.objects.first()
        if not captcha:
            captcha = Captcha.objects.create(value=str(random.randint(1000, 9999)))
        
        # Step 4: Create the order using create_order function
        print("\n📝 Creating order through create_order function...")
        payer_id = f'TEST_PAYER_{random.randint(1000, 9999)}'
        created_order = create_order(
            invoice=invoice,
            payer_id=payer_id,
            customer=client,
            status='New',
            name=name,
            extra=1
        )
        
        # create_order returns the game-specific order, not the base order
        if isinstance(created_order, LeagueOfLegendsDivisionOrder):
            lol_order = created_order
            base_order = lol_order.order
        else:
            # Fallback: try to get the base order
            base_order = created_order
            lol_order = LeagueOfLegendsDivisionOrder.objects.get(order=base_order)
        
        print(f"   ✅ Order created successfully!")
        print(f"   Base Order ID: {base_order.id}")
        print(f"   Order Name: {base_order.name}")
        print(f"   Price: ${base_order.price:.2f}")
        
        # Fix: Set real_order_price and update actual_price
        # The create_order function sets actual_price=0 for new orders
        # We need to set real_order_price and call update_actual_price()
        base_order.real_order_price = base_order.price
        base_order.save()
        
        # Update actual_price using the order's update method
        base_order.update_actual_price()
        base_order.refresh_from_db()
        
        print(f"   Actual Price: ${base_order.actual_price:.2f}")
        print(f"   Real Order Price: ${base_order.real_order_price:.2f}")
        
        print(f"\n📊 Order Details:")
        print(f"   Current Rank: {lol_order.current_rank} (PK: {lol_order.current_rank.pk})")
        print(f"   Current Division: {lol_order.current_division} ({'IV' if lol_order.current_division == 1 else 'III' if lol_order.current_division == 2 else 'II' if lol_order.current_division == 3 else 'I'})")
        print(f"   Current Marks: {lol_order.current_marks} ({'0-20' if lol_order.current_marks == 0 else '21-40' if lol_order.current_marks == 1 else '41-60' if lol_order.current_marks == 2 else '61-80' if lol_order.current_marks == 3 else '81-99' if lol_order.current_marks == 4 else 'SERIES'})")
        print(f"   Desired Rank: {lol_order.desired_rank} (PK: {lol_order.desired_rank.pk})")
        print(f"   Desired Division: {lol_order.desired_division} ({'IV' if lol_order.desired_division == 1 else 'III' if lol_order.desired_division == 2 else 'II' if lol_order.desired_division == 3 else 'I'})")
        
        # Step 6: Test the pricing function
        print(f"\n🧮 Testing get_order_price() function...")
        try:
            price_result = lol_order.get_order_price()
            
            print(f"   ✅ Price calculation successful!")
            print(f"   Booster Price: ${price_result['booster_price']:.2f}")
            print(f"   Percent for View: {price_result['percent_for_view']}%")
            print(f"   Main Price: ${price_result['main_price']:.2f}")
            print(f"   Percent: {price_result['percent']}%")
            
            # Verify prices are positive
            if price_result['booster_price'] > 0:
                print(f"   ✅ Booster price is positive")
            else:
                print(f"   ⚠️  Booster price is zero or negative")
            
            return {
                'base_order': base_order,
                'lol_order': lol_order,
                'calculated_price': calculated_price,
                'base_order_price': base_order.price,
                'actual_price': base_order.actual_price,
                'real_order_price': base_order.real_order_price,
                'price_result': price_result,
                'success': True
            }
            
        except Exception as e:
            print(f"   ❌ Error calculating price: {e}")
            import traceback
            traceback.print_exc()
            return {
                'base_order': base_order,
                'lol_order': lol_order,
                'calculated_price': calculated_price,
                'base_order_price': base_order.price,
                'actual_price': base_order.actual_price,
                'real_order_price': base_order.real_order_price,
                'price_result': None,
                'error': str(e),
                'success': False
            }
        
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': str(e)
        }

def check_pricing_entry(game_key, service_id, price):
    """Check if price exists in PricingEntry model"""
    try:
        entry = PricingEntry.objects.get(game_key=game_key, service_id=service_id)
        entry_price = float(entry.price)  # Convert Decimal to float
        price_float = float(price)  # Ensure price is float
        print(f"   📋 PricingEntry found: ${entry_price:.2f}")
        if abs(entry_price - price_float) < 0.01:
            print(f"   ✅ Price matches PricingEntry")
        else:
            print(f"   ⚠️  Price differs from PricingEntry (${entry_price:.2f} vs ${price_float:.2f})")
        return entry
    except PricingEntry.DoesNotExist:
        print(f"   ℹ️  No PricingEntry found for {game_key} service {service_id}")
        return None

def main():
    print("=" * 60)
    print("🎮 League of Legends Realistic Pricing Test")
    print("=" * 60)
    
    # Get or create test client
    client = get_or_create_test_client()
    print(f"\n✅ Test client: {client.username}")
    
    # Get ranks (using lowercase ranks that have pricing data)
    print("\n📋 Getting ranks...")
    iron_rank = get_rank_by_name('iron')
    silver_rank = get_rank_by_name('silver')
    gold_rank = get_rank_by_name('gold')
    platinum_rank = get_rank_by_name('platinum')
    diamond_rank = get_rank_by_name('diamond')
    
    print(f"   Iron: PK={iron_rank.pk} ({iron_rank.rank_name})")
    print(f"   Silver: PK={silver_rank.pk} ({silver_rank.rank_name})")
    print(f"   Gold: PK={gold_rank.pk} ({gold_rank.rank_name})")
    print(f"   Platinum: PK={platinum_rank.pk} ({platinum_rank.rank_name})")
    print(f"   Diamond: PK={diamond_rank.pk} ({diamond_rank.rank_name})")
    
    # Test cases
    test_cases = [
        {
            'name': 'Iron IV (0 LP) → Silver I (100 LP)',
            'current_rank': iron_rank,
            'current_division': 1,  # IV
            'current_marks': 0,  # 0-20 LP
            'desired_rank': silver_rank,
            'desired_division': 4,  # I
        },
        {
            'name': 'Gold II (50 LP) → Platinum IV (0 LP)',
            'current_rank': gold_rank,
            'current_division': 2,  # II
            'current_marks': 2,  # 41-60 LP (approximate 50 LP)
            'desired_rank': platinum_rank,
            'desired_division': 1,  # IV
        },
        {
            'name': 'Diamond IV (20 LP) → Diamond I (80 LP)',
            'current_rank': diamond_rank,
            'current_division': 1,  # IV
            'current_marks': 0,  # 0-20 LP
            'desired_rank': diamond_rank,
            'desired_division': 4,  # I
        }
    ]
    
    results = []
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'#'*60}")
        print(f"Test Case {i}/{len(test_cases)}")
        print(f"{'#'*60}")
        
        result = create_realistic_order(
            client=client,
            current_rank=test_case['current_rank'],
            current_division=test_case['current_division'],
            current_marks=test_case['current_marks'],
            desired_rank=test_case['desired_rank'],
            desired_division=test_case['desired_division'],
            test_case_name=test_case['name']
        )
        
        results.append({
            'test_case': test_case['name'],
            **result
        })
        
        # Check PricingEntry (optional - for admin dashboard integration)
        if result.get('success') and result.get('base_order'):
            print(f"\n🔍 Checking PricingEntry model...")
            # Note: PricingEntry is for admin dashboard, not for order pricing
            # But we can check if there's any correlation
            check_pricing_entry('lol', 1, result['base_order_price'])
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    successful_tests = sum(1 for r in results if r.get('success'))
    total_tests = len(results)
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    
    if successful_tests > 0:
        print(f"\n💰 Price Comparison:")
        print(f"{'Test Case':<50} {'Base Price':<15} {'Actual Price':<15} {'Booster Price':<15}")
        print(f"{'-'*95}")
        
        for i, result in enumerate(results, 1):
            if result.get('success'):
                base_price = result.get('base_order_price', 0)
                actual_price = result.get('actual_price', 0)
                booster_price = result.get('price_result', {}).get('booster_price', 0) if result.get('price_result') else 0
                print(f"{result['test_case']:<50} ${base_price:<14.2f} ${actual_price:<14.2f} ${booster_price:<14.2f}")
        
        # Verify price scaling
        print(f"\n📈 Price Scaling Analysis:")
        prices = [r.get('base_order_price', 0) for r in results if r.get('success')]
        if len(prices) > 1:
            print(f"   Prices: {[f'${p:.2f}' for p in prices]}")
            
            # Check if prices increase with rank difference
            rank_differences = []
            for i, result in enumerate(results):
                if result.get('success') and result.get('lol_order'):
                    current = result['lol_order'].current_rank.pk
                    desired = result['lol_order'].desired_rank.pk
                    rank_differences.append(desired - current)
            
            print(f"   Rank differences: {rank_differences}")
            
            # Iron to Silver (rank 1 to 3) = difference 2
            # Gold to Platinum (rank 4 to 5) = difference 1
            # Diamond to Diamond (rank 7 to 7) = difference 0
            
            if prices[0] > prices[2] and prices[1] > prices[2]:
                print(f"   ✅ Prices scale correctly (higher rank differences = higher prices)")
            else:
                print(f"   ⚠️  Price scaling may need review")
        
        # Verify all prices are positive
        all_positive = all(r.get('base_order_price', 0) > 0 for r in results if r.get('success'))
        if all_positive:
            print(f"\n   ✅ All prices are positive")
        else:
            print(f"\n   ⚠️  Some prices are zero or negative")
    
    # Cleanup test orders
    print(f"\n🧹 Cleaning up test orders...")
    from django.apps import apps
    for result in results:
        if result.get('base_order'):
            try:
                # Check if WorldOfWarcraft app is installed before cleanup
                if apps.is_installed('WorldOfWarcraft'):
                    try:
                        result['base_order'].delete()
                        print(f"   ✅ Deleted order: {result.get('test_case', 'Unknown')}")
                    except Exception as e:
                        # Handle WorldOfWarcraft table errors gracefully
                        if 'WorldOfWarcraft' in str(e) or 'relation' in str(e).lower():
                            print(f"   ⚠️  Warning during cleanup (non-critical): {e}")
                            print(f"   ✅ Order cleanup skipped (unrelated game model)")
                        else:
                            raise
                else:
                    result['base_order'].delete()
                    print(f"   ✅ Deleted order: {result.get('test_case', 'Unknown')}")
            except Exception as e:
                print(f"   ⚠️  Error deleting order: {e}")
    
    print(f"\n✅ Testing complete!")

if __name__ == '__main__':
    main()

