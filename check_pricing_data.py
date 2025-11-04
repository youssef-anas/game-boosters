#!/usr/bin/env python
"""
Check League of Legends pricing data structure
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
django.setup()

from leagueOfLegends.models import LeagueOfLegendsTier, LeagueOfLegendsMark, LeagueOfLegendsRank
from leagueOfLegends.models import get_lol_divisions_data, get_lol_marks_data

print("=" * 60)
print("League of Legends Pricing Data Check")
print("=" * 60)

print(f"\n📊 Database Counts:")
print(f"   Ranks: {LeagueOfLegendsRank.objects.count()}")
print(f"   Tiers: {LeagueOfLegendsTier.objects.count()}")
print(f"   Marks: {LeagueOfLegendsMark.objects.count()}")

print(f"\n📋 Ranks List:")
for rank in LeagueOfLegendsRank.objects.all().order_by('id'):
    print(f"   ID {rank.id}: {rank.rank_name}")

print(f"\n💰 Pricing Data Structure:")

# Get division data
divs = get_lol_divisions_data()
print(f"\n   Division Data Length: {len(divs)}")
if divs:
    print(f"   First division entry: {divs[0]}")
    print(f"   Last division entry: {divs[-1] if len(divs) > 1 else 'N/A'}")
    print(f"   Total division entries: {sum(len(d) for d in divs)}")
    
    # Flatten and check
    flattened = [item for sublist in divs for item in sublist]
    flattened.insert(0, 0)
    print(f"   Flattened data length: {len(flattened)}")
    print(f"   First 10 flattened values: {flattened[:10]}")
else:
    print("   ⚠️  No division data found!")

# Get marks data
marks = get_lol_marks_data()
print(f"\n   Marks Data Length: {len(marks)}")
if marks:
    marks.insert(0, [0, 0, 0, 0, 0, 0])
    print(f"   Marks data with padding: {len(marks)} entries")
    print(f"   First marks entry: {marks[0]}")
    print(f"   Second marks entry: {marks[1] if len(marks) > 1 else 'N/A'}")
    
    # Check if we have enough data for rank 9 (Iron)
    if len(marks) > 9:
        print(f"   Marks for rank 9 (Iron): {marks[9]}")
    else:
        print(f"   ⚠️  Not enough marks data for rank 9 (Iron)!")
else:
    print("   ⚠️  No marks data found!")

# Test the calculation that's failing
print(f"\n🔍 Testing Calculation Logic:")
print(f"   Iron rank ID: 9")
print(f"   Silver rank ID: 10")
print(f"   Current division: 1 (IV)")
print(f"   Desired division: 4 (I)")
print(f"   Current marks: 0")

# Calculate start_division and end_division
current_rank = 9
reached_rank = 9  # Start at current rank
current_division = 1
reached_division = 1
desired_rank = 10
desired_division = 4

start_division = ((current_rank - 1) * 4) + current_division
end_division = ((desired_rank - 1) * 4) + desired_division

print(f"\n   Calculation:")
print(f"   start_division = (({current_rank} - 1) * 4) + {current_division} = {start_division}")
print(f"   end_division = (({desired_rank} - 1) * 4) + {desired_division} = {end_division}")

if divs:
    flattened = [item for sublist in divs for item in sublist]
    flattened.insert(0, 0)
    print(f"\n   Flattened data length: {len(flattened)}")
    print(f"   Trying to access indices [{start_division}:{end_division}]")
    
    if end_division > len(flattened):
        print(f"   ❌ ERROR: end_division ({end_division}) > flattened length ({len(flattened)})")
        print(f"   Need to add more pricing data!")
    else:
        print(f"   ✅ Indices are within range")
        sublist = flattened[start_division:end_division]
        print(f"   Extracted sublist: {sublist}")
        print(f"   Sum: {sum(sublist)}")

if marks:
    marks_with_padding = marks.copy()
    marks_with_padding.insert(0, [0, 0, 0, 0, 0, 0])
    print(f"\n   Marks data length: {len(marks_with_padding)}")
    if current_rank < len(marks_with_padding):
        print(f"   ✅ Can access marks[{current_rank}] = {marks_with_padding[current_rank]}")
    else:
        print(f"   ❌ ERROR: Cannot access marks[{current_rank}] (length: {len(marks_with_padding)})")

print("\n" + "=" * 60)

