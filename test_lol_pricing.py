#!/usr/bin/env python
"""
Test script for League of Legends pricing function
Tests get_order_price() with various rank and LP combinations
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsRank
from accounts.models import BaseOrder, BaseUser, Captcha
from games.models import Game
from django.contrib.contenttypes.models import ContentType
import random

def find_or_create_rank(rank_name):
    """Find or create a League of Legends rank"""
    rank, created = LeagueOfLegendsRank.objects.get_or_create(
        rank_name=rank_name,
        defaults={'rank_name': rank_name}
    )
    return rank

def get_or_create_test_client():
    """Get or create a test client"""
    client, created = BaseUser.objects.get_or_create(
        username='test_client_pricing',
        defaults={
            'email': 'test_client_pricing@test.com',
            'is_customer': True,
            'is_active': True
        }
    )
    if created:
        client.set_password('test123')
        client.save()
    return client

def get_or_create_test_game():
    """Get or create League of Legends game"""
    game, created = Game.objects.get_or_create(
        name='League of Legends',
        defaults={'link': 'lol'}
    )
    return game

def create_test_order(client, game, current_rank, current_division, current_marks,
                     desired_rank, desired_division, order_name, test_case_name):
    """Create a test order with the given parameters"""
    try:
        # Get or create captcha
        captcha = Captcha.objects.first()
        if not captcha:
            captcha = Captcha.objects.create(value=str(random.randint(1000, 9999)))
        
        # Create base order
        base_order = BaseOrder.objects.create(
            name=order_name,
            details=f'Test order: {test_case_name}',
            game=game,
            game_type='D',
            price=100.00,  # Placeholder, will be calculated
            actual_price=100.00,
            real_order_price=100.00,
            money_owed=80.00,
            invoice=f'TEST_INVOICE_{order_name}',
            status='New',
            customer=client,
            booster=None,
            customer_gamename='TestSummoner',
            customer_username='testuser123',
            customer_password='testpass123',
            customer_server='EUW',
            captcha=captcha,
            payer_id='TEST_PAYER_ID',
            is_done=False,
            is_drop=False,
            is_extended=False,
            data_correct=True,
            approved=True,
            duo_boosting=False,
            select_booster=False,
            turbo_boost=False,
            streaming=False
        )
        
        # Create League of Legends specific order
        lol_order = LeagueOfLegendsDivisionOrder.objects.create(
            order=base_order,
            current_rank=current_rank,
            desired_rank=desired_rank,
            current_division=current_division,
            desired_division=desired_division,
            current_marks=current_marks,
            reached_marks=0,  # Start at 0
            reached_rank=current_rank,  # Start at current rank
            reached_division=current_division,
            select_champion=False
        )
        
        # Set content type
        content_type = ContentType.objects.get_for_model(LeagueOfLegendsDivisionOrder)
        base_order.content_type = content_type
        base_order.object_id = lol_order.pk
        base_order.save()
        
        return lol_order
        
    except Exception as e:
        print(f"❌ Error creating test order '{test_case_name}': {e}")
        return None

def test_pricing_function(lol_order, test_case_name):
    """Test the get_order_price() function for a given order"""
    print(f"\n{'='*60}")
    print(f"Test Case: {test_case_name}")
    print(f"{'='*60}")
    
    try:
        # Check for null values
        print(f"\n📊 Order Details:")
        print(f"   Current Rank: {lol_order.current_rank} (PK: {lol_order.current_rank.pk if lol_order.current_rank else 'NULL'})")
        print(f"   Current Division: {lol_order.current_division} ({'IV' if lol_order.current_division == 1 else 'III' if lol_order.current_division == 2 else 'II' if lol_order.current_division == 3 else 'I'})")
        print(f"   Current Marks: {lol_order.current_marks} ({'0-20' if lol_order.current_marks == 0 else '21-40' if lol_order.current_marks == 1 else '41-60' if lol_order.current_marks == 2 else '61-80' if lol_order.current_marks == 3 else '81-99' if lol_order.current_marks == 4 else 'SERIES'})")
        print(f"   Desired Rank: {lol_order.desired_rank} (PK: {lol_order.desired_rank.pk if lol_order.desired_rank else 'NULL'})")
        print(f"   Desired Division: {lol_order.desired_division} ({'IV' if lol_order.desired_division == 1 else 'III' if lol_order.desired_division == 2 else 'II' if lol_order.desired_division == 3 else 'I'})")
        
        # Check for null values
        null_checks = []
        if lol_order.current_rank is None:
            null_checks.append("current_rank is NULL")
        if lol_order.desired_rank is None:
            null_checks.append("desired_rank is NULL")
        if lol_order.current_division is None:
            null_checks.append("current_division is NULL")
        if lol_order.desired_division is None:
            null_checks.append("desired_division is NULL")
        if lol_order.current_marks is None:
            null_checks.append("current_marks is NULL")
        
        if null_checks:
            print(f"\n⚠️  WARNING: Null values detected:")
            for check in null_checks:
                print(f"   - {check}")
        else:
            print(f"\n✅ No null values detected")
        
        # Call the pricing function
        print(f"\n💰 Calculating price...")
        result = lol_order.get_order_price()
        
        print(f"\n✅ Price Calculation Results:")
        print(f"   Booster Price: ${result.get('booster_price', 'N/A'):.2f}")
        print(f"   Percent for View: {result.get('percent_for_view', 'N/A')}%")
        print(f"   Main Price: ${result.get('main_price', 'N/A'):.2f}")
        print(f"   Percent: {result.get('percent', 'N/A')}%")
        
        return result
        
    except AttributeError as e:
        print(f"\n❌ AttributeError: {e}")
        print(f"   This might indicate missing rank or division data")
        return None
    except IndexError as e:
        print(f"\n❌ IndexError: {e}")
        print(f"   This might indicate missing pricing data in database")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("🎮 League of Legends Pricing Function Test")
    print("=" * 60)
    
    # Get or create test client and game
    client = get_or_create_test_client()
    game = get_or_create_test_game()
    
    # Find or create ranks - Use lowercase ranks that have pricing data
    print("\n📋 Setting up ranks...")
    # Try to find existing ranks first (lowercase have pricing data)
    iron_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact='iron').first()
    if not iron_rank:
        iron_rank = find_or_create_rank('iron')
    
    silver_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact='silver').first()
    if not silver_rank:
        silver_rank = find_or_create_rank('silver')
    
    gold_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact='gold').first()
    if not gold_rank:
        gold_rank = find_or_create_rank('gold')
    
    platinum_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact='platinum').first()
    if not platinum_rank:
        platinum_rank = find_or_create_rank('platinum')
    
    diamond_rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact='diamond').first()
    if not diamond_rank:
        diamond_rank = find_or_create_rank('diamond')
    
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
            'order_name': 'TEST_IRON_TO_SILVER'
        },
        {
            'name': 'Gold II (50 LP) → Platinum IV (0 LP)',
            'current_rank': gold_rank,
            'current_division': 2,  # II
            'current_marks': 2,  # 41-60 LP (approximate 50 LP)
            'desired_rank': platinum_rank,
            'desired_division': 1,  # IV
            'order_name': 'TEST_GOLD_TO_PLATINUM'
        },
        {
            'name': 'Diamond IV (20 LP) → Diamond I (80 LP)',
            'current_rank': diamond_rank,
            'current_division': 1,  # IV
            'current_marks': 0,  # 0-20 LP
            'desired_rank': diamond_rank,
            'desired_division': 4,  # I
            'order_name': 'TEST_DIAMOND_IV_TO_I'
        }
    ]
    
    results = []
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n{'#'*60}")
        print(f"Running Test Case {i}/{len(test_cases)}")
        print(f"{'#'*60}")
        
        # Create test order
        lol_order = create_test_order(
            client=client,
            game=game,
            current_rank=test_case['current_rank'],
            current_division=test_case['current_division'],
            current_marks=test_case['current_marks'],
            desired_rank=test_case['desired_rank'],
            desired_division=test_case['desired_division'],
            order_name=test_case['order_name'],
            test_case_name=test_case['name']
        )
        
        if lol_order:
            # Test pricing function
            result = test_pricing_function(lol_order, test_case['name'])
            results.append({
                'test_case': test_case['name'],
                'result': result,
                'success': result is not None
            })
            
            # Clean up test order
            try:
                lol_order.order.delete()
            except:
                pass
        else:
            results.append({
                'test_case': test_case['name'],
                'result': None,
                'success': False
            })
    
    # Summary
    print(f"\n\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    successful_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    
    if successful_tests > 0:
        print(f"\n💰 Price Comparison:")
        for i, result in enumerate(results, 1):
            if result['success'] and result['result']:
                price = result['result'].get('booster_price', 0)
                print(f"   {i}. {result['test_case']}: ${price:.2f}")
        
        # Check price scaling consistency
        print(f"\n📈 Price Scaling Analysis:")
        prices = [r['result'].get('booster_price', 0) for r in results if r['success'] and r['result']]
        if len(prices) > 1:
            print(f"   Prices: {[f'${p:.2f}' for p in prices]}")
            if prices[0] < prices[1] < prices[2] or prices[0] < prices[2]:
                print(f"   ✅ Prices appear to scale correctly (higher ranks = higher prices)")
            else:
                print(f"   ⚠️  Price scaling may need review")
    
    print(f"\n✅ Testing complete!")

if __name__ == '__main__':
    main()


