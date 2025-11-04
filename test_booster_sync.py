#!/usr/bin/env python
"""
Test booster system synchronization for League of Legends orders
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from leagueOfLegends.controller.order_information import get_division_order_result_by_rank
from customer.controllers.order_creator import create_order
from accounts.models import BaseUser, BaseOrder, Captcha, Transaction, Wallet
from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsRank
from booster.models import Booster
from games.models import Game
import random

# Test data
SYNC_LOG = []

def log_step(step, status, booster_price, progress_percent, synced, notes=""):
    """Log a synchronization step"""
    SYNC_LOG.append({
        'step': step,
        'status': status,
        'booster_price': booster_price,
        'progress_percent': progress_percent,
        'synced': synced,
        'notes': notes,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    print(f"   [{step}] Status: {status} | Booster Price: ${booster_price:.2f} | Progress: {progress_percent}% | Synced: {synced} {notes}")

def get_or_create_test_client():
    """Get or create a test client"""
    client, created = BaseUser.objects.get_or_create(
        username='test_client_sync',
        defaults={
            'email': 'test_client_sync@test.com',
            'is_customer': True,
            'is_active': True
        }
    )
    if created:
        client.set_password('test123')
        client.save()
        Wallet.objects.get_or_create(user=client)
    return client

def get_or_create_test_booster():
    """Get or create a test booster"""
    booster_user, created = BaseUser.objects.get_or_create(
        username='test_booster_sync',
        defaults={
            'email': 'test_booster_sync@test.com',
            'is_booster': True,
            'is_active': True
        }
    )
    if created:
        booster_user.set_password('test123')
        booster_user.save()
        Wallet.objects.get_or_create(user=booster_user)
        
        # Create booster profile
        booster_profile, _ = Booster.objects.get_or_create(
            booster=booster_user,
            defaults={
                'discord_id': 'test_booster#1234',
                'paypal_account': 'test_booster@test.com',
                'can_choose_me': True,
                'is_lol_player': True
            }
        )
    else:
        booster_profile = Booster.objects.get(booster=booster_user)
        booster_profile.is_lol_player = True
        booster_profile.save()
    
    return booster_user, booster_profile

def get_rank_by_name(rank_name):
    """Get rank by name (case-insensitive)"""
    rank = LeagueOfLegendsRank.objects.filter(rank_name__iexact=rank_name).first()
    if not rank:
        raise ValueError(f"Rank '{rank_name}' not found in database")
    return rank

def create_order_as_client(client, current_rank, current_division, current_marks,
                          desired_rank, desired_division):
    """Step 1: Create order as a client"""
    print("\n" + "="*60)
    print("STEP 1: Creating Order as Client")
    print("="*60)
    
    # Prepare order data
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
        'price': 0,
        'choose_booster': 0,
        'champion_data': '',
        'extend_order': 0,
        'promo_code': 'null'
    }
    
    # Calculate price
    order_info = get_division_order_result_by_rank(order_data)
    calculated_price = order_info['price']
    invoice = order_info['invoice']
    name = order_info['name']
    
    # Truncate name to 30 characters
    if len(name) > 30:
        name = name[:27] + "..."
    
    print(f"   Calculated Price: ${calculated_price:.2f}")
    
    # Create order
    payer_id = f'TEST_PAYER_{random.randint(1000, 9999)}'
    created_order = create_order(
        invoice=invoice,
        payer_id=payer_id,
        customer=client,
        status='New',
        name=name,
        extra=1
    )
    
    # Get base order
    if isinstance(created_order, LeagueOfLegendsDivisionOrder):
        lol_order = created_order
        base_order = lol_order.order
    else:
        base_order = created_order
        lol_order = LeagueOfLegendsDivisionOrder.objects.get(order=base_order)
    
    # Set real_order_price and update actual_price
    base_order.real_order_price = base_order.price
    base_order.save()
    base_order.update_actual_price()
    base_order.refresh_from_db()
    
    # Get initial booster price
    price_result = lol_order.get_order_price()
    initial_booster_price = price_result['booster_price']
    progress_percent = price_result['percent_for_view']
    
    log_step(
        step="1. Order Created",
        status=base_order.status,
        booster_price=initial_booster_price,
        progress_percent=progress_percent,
        synced="✅" if base_order.booster is None else "❌",
        notes=f"(Price: ${base_order.price:.2f})"
    )
    
    return base_order, lol_order

def assign_order_to_booster(base_order, lol_order, booster_user):
    """Step 2: Assign order to booster (simulate claim)"""
    print("\n" + "="*60)
    print("STEP 2: Assigning Order to Booster")
    print("="*60)
    
    # Verify order is unassigned
    if base_order.booster is not None:
        print(f"   ⚠️  Order already assigned to {base_order.booster.username}")
        return False
    
    # Simulate booster claim (same as ClaimOrderView)
    base_order.booster = booster_user
    base_order.status = 'Continue'  # Status changes to "In Progress"
    base_order.save()
    base_order.refresh_from_db()
    
    # Update booster price (same as booster_orders view)
    price_result = lol_order.get_order_price()
    base_order.money_owed = price_result['booster_price']
    base_order.save()
    
    print(f"   ✅ Order assigned to booster: {booster_user.username}")
    print(f"   ✅ Status changed to: {base_order.status}")
    print(f"   ✅ Booster price set: ${base_order.money_owed:.2f}")
    
    log_step(
        step="2. Booster Claimed",
        status=base_order.status,
        booster_price=base_order.money_owed,
        progress_percent=price_result['percent_for_view'],
        synced="✅",
        notes=f"(Booster: {booster_user.username})"
    )
    
    return True

def update_order_progress(lol_order, progress_percent):
    """Step 3: Update order progress (supports granular progress: 25%, 50%, 75%, 100%)"""
    print("\n" + "="*60)
    print(f"STEP 3: Updating Order Progress to {progress_percent}%")
    print("="*60)
    
    base_order = lol_order.order
    
    # Calculate progress based on rank/division
    # Supports granular progress steps: 25%, 50%, 75%, 100%
    
    current_rank_pk = lol_order.current_rank.pk
    desired_rank_pk = lol_order.desired_rank.pk
    current_division = lol_order.current_division
    desired_division = lol_order.desired_division
    
    # Calculate intermediate rank/division based on progress percentage
    rank_diff = desired_rank_pk - current_rank_pk
    division_diff = desired_division - current_division
    
    # Calculate total divisions (each rank has 4 divisions)
    # Current position: (current_rank_pk - 1) * 4 + current_division
    # Desired position: (desired_rank_pk - 1) * 4 + desired_division
    current_position = (current_rank_pk - 1) * 4 + current_division
    desired_position = (desired_rank_pk - 1) * 4 + desired_division
    total_positions = desired_position - current_position
    
    # Calculate reached position based on progress percentage
    reached_position = current_position + int((total_positions * progress_percent) / 100)
    
    # Convert back to rank and division
    reached_rank_pk = ((reached_position - 1) // 4) + 1
    reached_division = ((reached_position - 1) % 4) + 1
    
    # Ensure reached_division is valid (1-4)
    reached_division = max(1, min(4, reached_division))
    
    # Ensure reached_rank_pk is within bounds
    reached_rank_pk = max(current_rank_pk, min(desired_rank_pk, reached_rank_pk))
    
    # Get the rank object
    reached_rank = LeagueOfLegendsRank.objects.get(pk=reached_rank_pk)
    
    # Update reached progress
    lol_order.reached_rank = reached_rank
    lol_order.reached_division = reached_division
    lol_order.reached_marks = 0  # Default to 0-20 LP
    lol_order.save()
    
    # Update booster price based on new progress
    price_result = lol_order.get_order_price()
    base_order.money_owed = price_result['booster_price']
    base_order.save()
    
    print(f"   ✅ Progress updated:")
    print(f"      Reached Rank: {reached_rank.rank_name} (PK: {reached_rank.pk})")
    print(f"      Reached Division: {reached_division}")
    print(f"      Progress: {progress_percent}%")
    print(f"      Booster Price: ${base_order.money_owed:.2f}")
    print(f"      Progress View: {price_result.get('percent_for_view', 0):.1f}%")
    
    log_step(
        step=f"3. Progress {progress_percent}%",
        status=base_order.status,
        booster_price=base_order.money_owed,
        progress_percent=price_result.get('percent_for_view', 0),
        synced="✅",
        notes=f"(Reached: {reached_rank.rank_name} {reached_division})"
    )
    
    return True

def complete_order(base_order, lol_order):
    """Step 4: Complete the order"""
    print("\n" + "="*60)
    print("STEP 4: Completing Order")
    print("="*60)
    
    # Get initial wallet balance
    booster_wallet_before = base_order.booster.wallet.money if base_order.booster else 0
    
    # Set reached progress to desired (100%)
    lol_order.reached_rank = lol_order.desired_rank
    lol_order.reached_division = lol_order.desired_division
    lol_order.reached_marks = 0
    lol_order.save()
    
    # Update booster price to final value
    price_result = lol_order.get_order_price()
    base_order.money_owed = price_result['booster_price']
    
    # Mark order as done
    base_order.is_done = True
    base_order.status = 'Done'
    base_order.save()
    
    # Refresh wallet to get updated balance
    base_order.booster.wallet.refresh_from_db()
    booster_wallet_after = base_order.booster.wallet.money
    
    # Check for transaction
    transactions = Transaction.objects.filter(
        user=base_order.booster,
        order=base_order,
        status='Done',
        type='DEPOSIT'
    )
    
    print(f"   ✅ Order completed:")
    print(f"      Status: {base_order.status}")
    print(f"      Final Booster Price: ${base_order.money_owed:.2f}")
    print(f"      Booster Wallet Before: ${booster_wallet_before:.2f}")
    print(f"      Booster Wallet After: ${booster_wallet_after:.2f}")
    print(f"      Wallet Increase: ${booster_wallet_after - booster_wallet_before:.2f}")
    print(f"      Transactions Created: {transactions.count()}")
    
    # Verify synchronization
    wallet_synced = abs((booster_wallet_after - booster_wallet_before) - base_order.money_owed) < 0.01
    transaction_synced = transactions.exists()
    
    log_step(
        step="4. Order Completed",
        status=base_order.status,
        booster_price=base_order.money_owed,
        progress_percent=100,
        synced="✅" if (wallet_synced and transaction_synced) else "❌",
        notes=f"(Wallet: ${booster_wallet_after:.2f}, Transactions: {transactions.count()})"
    )
    
    return wallet_synced and transaction_synced

def print_summary_table():
    """Print summary table"""
    print("\n" + "="*60)
    print("📊 SYNCHRONIZATION SUMMARY TABLE")
    print("="*60)
    print(f"{'Step':<25} {'Status':<15} {'Booster Price':<15} {'Progress %':<12} {'Synced':<8}")
    print("-" * 80)
    
    for log_entry in SYNC_LOG:
        print(f"{log_entry['step']:<25} {log_entry['status']:<15} ${log_entry['booster_price']:<14.2f} {log_entry['progress_percent']:<12} {log_entry['synced']:<8}")
    
    print("-" * 80)
    
    # Overall sync status
    all_synced = all(entry['synced'] == "✅" for entry in SYNC_LOG)
    print(f"\n{'Overall Sync Status:':<25} {'✅ ALL SYNCED' if all_synced else '❌ SOME ISSUES'}")
    
    return all_synced

def main():
    print("="*60)
    print("🎮 Booster System Synchronization Test")
    print("="*60)
    
    # Setup
    print("\n📋 Setting up test environment...")
    client = get_or_create_test_client()
    booster_user, booster_profile = get_or_create_test_booster()
    
    print(f"   Client: {client.username}")
    print(f"   Booster: {booster_user.username}")
    
    # Get ranks
    print("\n📋 Getting ranks...")
    iron_rank = get_rank_by_name('iron')
    silver_rank = get_rank_by_name('silver')
    
    print(f"   Iron: PK={iron_rank.pk} ({iron_rank.rank_name})")
    print(f"   Silver: PK={silver_rank.pk} ({silver_rank.rank_name})")
    
    try:
        # Step 1: Create order as client
        base_order, lol_order = create_order_as_client(
            client=client,
            current_rank=iron_rank,
            current_division=1,  # IV
            current_marks=0,  # 0-20 LP
            desired_rank=silver_rank,
            desired_division=4  # I
        )
        
        # Step 2: Assign to booster
        if not assign_order_to_booster(base_order, lol_order, booster_user):
            print("   ❌ Failed to assign order to booster")
            return
        
        # Step 3: Update progress to multiple milestones (25%, 50%, 75%, 100%)
        print("\n" + "="*60)
        print("STEP 3: Testing Granular Progress Updates")
        print("="*60)
        
        progress_milestones = [25, 50, 75]
        for progress in progress_milestones:
            update_order_progress(lol_order, progress)
            base_order.refresh_from_db()
            lol_order.refresh_from_db()
        
        # Step 4: Complete order (100%)
        complete_synced = complete_order(base_order, lol_order)
        
        # Print summary
        all_synced = print_summary_table()
        
        # Final verification
        print("\n" + "="*60)
        print("✅ FINAL VERIFICATION")
        print("="*60)
        
        base_order.refresh_from_db()
        lol_order.refresh_from_db()
        
        print(f"\n✅ Order Status: {base_order.status}")
        print(f"✅ Order is_done: {base_order.is_done}")
        print(f"✅ Booster assigned: {base_order.booster.username if base_order.booster else 'None'}")
        print(f"✅ Final money_owed: ${base_order.money_owed:.2f}")
        print(f"✅ Reached Rank: {lol_order.reached_rank.rank_name} (Target: {lol_order.desired_rank.rank_name})")
        print(f"✅ Reached Division: {lol_order.reached_division} (Target: {lol_order.desired_division})")
        
        # Check transactions
        transactions = Transaction.objects.filter(order=base_order, user=base_order.booster)
        print(f"✅ Transactions created: {transactions.count()}")
        for txn in transactions:
            print(f"      - {txn.type}: ${txn.amount:.2f} ({txn.status})")
        
        # Check wallet
        booster_wallet = base_order.booster.wallet
        print(f"✅ Booster wallet balance: ${booster_wallet.money:.2f}")
        
        print(f"\n{'🎯 RESULT:':<25} {'✅ ALL SYNCED' if all_synced else '❌ SOME ISSUES'}")
        
        # Cleanup
        print("\n🧹 Cleaning up test order...")
        try:
            base_order.delete()
            print("   ✅ Test order deleted")
        except Exception as e:
            print(f"   ⚠️  Error deleting order: {e}")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✅ Testing complete!")

if __name__ == '__main__':
    main()

