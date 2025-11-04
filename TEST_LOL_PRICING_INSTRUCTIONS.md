# League of Legends Pricing Function Test Instructions

## Running the Test

You can run the test script in one of the following ways:

### Option 1: Direct Python Execution (Recommended)
```bash
docker-compose exec web python test_lol_pricing.py
```

### Option 2: Django Shell
```bash
docker-compose exec web python manage.py shell
```
Then in the shell:
```python
exec(open('test_lol_pricing.py').read())
```

### Option 3: Run locally (if Django is set up locally)
```bash
python test_lol_pricing.py
```

## What the Test Does

The test script will:

1. **Import Required Models:**
   - `LeagueOfLegendsDivisionOrder`
   - `LeagueOfLegendsRank`
   - `BaseOrder`
   - `BaseUser`
   - `Game`

2. **Create Test Orders:**
   - **Test Case 1:** Iron IV (0 LP) → Silver I (100 LP)
   - **Test Case 2:** Gold II (50 LP) → Platinum IV (0 LP)
   - **Test Case 3:** Diamond IV (20 LP) → Diamond I (80 LP)

3. **Test Pricing Function:**
   - Calls `get_order_price()` for each test order
   - Checks for null values in ranks, divisions, and marks
   - Catches and logs any errors (AttributeError, IndexError, etc.)
   - Prints calculated prices

4. **Verify Price Scaling:**
   - Compares prices across different rank combinations
   - Ensures higher ranks result in higher prices

## Expected Output

The test will print:
- Order details (ranks, divisions, marks)
- Null value checks
- Calculated prices (booster_price, percent_for_view, main_price, percent)
- Error messages if any issues occur
- Summary of all tests with price comparisons

## Troubleshooting

If you encounter errors:

1. **Missing Ranks:** The script will create ranks automatically if they don't exist
2. **Missing Pricing Data:** You may need to populate `LeagueOfLegendsTier` and `LeagueOfLegendsMark` tables with pricing data
3. **Database Issues:** Ensure your database is properly migrated and accessible

## Manual Test (Alternative)

If the script doesn't work, you can test manually in Django shell:

```python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameBoosterss.settings')
import django
django.setup()

from leagueOfLegends.models import LeagueOfLegendsDivisionOrder, LeagueOfLegendsRank
from accounts.models import BaseOrder, BaseUser
from games.models import Game

# Get ranks
iron = LeagueOfLegendsRank.objects.get(rank_name='Iron')
silver = LeagueOfLegendsRank.objects.get(rank_name='Silver')

# Create a test order (simplified)
# ... (create BaseOrder and LeagueOfLegendsDivisionOrder)

# Test pricing
order = LeagueOfLegendsDivisionOrder.objects.get(...)
result = order.get_order_price()
print(result)
```


