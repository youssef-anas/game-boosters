#!/bin/bash
# Script to apply csgo2 price function fixes on VPS
# Run this on your VPS: bash apply-fixes-vps.sh

set -e

echo "🔧 Applying csgo2 price function fixes..."

PROJECT_DIR="/opt/game-boosters"
cd "$PROJECT_DIR"

# Backup files first
echo "📦 Backing up files..."
cp csgo2/utils.py csgo2/utils.py.backup 2>/dev/null || true
cp csgo2/controller/order_information.py csgo2/controller/order_information.py.backup 2>/dev/null || true

# Fix csgo2/utils.py - replace entire file
echo "✅ Fixing csgo2/utils.py..."
cat > csgo2/utils.py << 'EOF'
from .models import Csgo2Tier, Csgo2PremierPrice, CsgoFaceitPrice

def get_division_prices():
    divisions = Csgo2Tier.objects.all().order_by('id')
    if not divisions.exists():
        # Return empty list of lists structure if no data
        return []
    divisions_data = [
        [division.from_I_to_I_next]
        for division in divisions
    ]
    return divisions_data

def get_premier_prices():
    premier_row = Csgo2PremierPrice.objects.all().first()
    if not premier_row:
        # Return list of zeros to prevent IndexError
        return [0, 0, 0, 0, 0, 0, 0]
    premier_prices = [
        premier_row.price_0_4999, premier_row.price_5000_7999, premier_row.price_8000_11999, 
        premier_row.price_12000_18999, premier_row.price_19000_20999, premier_row.price_21000_24999, 
        premier_row.price_25000_30000
    ]
    return premier_prices

def get_faceit_prices():
    faceit_prices = CsgoFaceitPrice.objects.all().first()
    if not faceit_prices:
        # Return list of zeros to prevent AttributeError
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    faceit_data = [
        0, faceit_prices.from_1_to_2, faceit_prices.from_2_to_3, faceit_prices.from_3_to_4, 
        faceit_prices.from_4_to_5, faceit_prices.from_5_to_6, faceit_prices.from_6_to_7, 
        faceit_prices.from_7_to_8, faceit_prices.from_8_to_9, faceit_prices.from_9_to_10
    ]
    return faceit_data
EOF

# Fix csgo2/controller/order_information.py using Python
echo "✅ Fixing csgo2/controller/order_information.py..."

python3 << 'PYFIX'
import re

file_path = "csgo2/controller/order_information.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Replace get_division_order_result_by_rank function section
old_section1 = """    # Read data from utils file
    division_price = get_division_prices()
    flattened_data = [item for sublist in division_price for item in sublist]
    flattened_data.insert(0,0)"""

new_section1 = """    # Read data from utils file
    division_price = get_division_prices()
    if division_price and isinstance(division_price, (list, tuple)):
        flattened_data = [item for sublist in division_price for item in sublist if isinstance(sublist, (list, tuple))]
    else:
        flattened_data = []
    flattened_data.insert(0, 0)"""

content = content.replace(old_section1, new_section1)

# Fix 2: Replace total_sum line
content = re.sub(
    r'(\s+)total_sum = sum\(sublist\)',
    r'\1total_sum = sum(sublist) if sublist else 0',
    content
)

# Fix 3: Replace class definition
old_class = """    division_prices_data = get_division_prices()
    division_prices = [item for sublist in division_prices_data for item in sublist]
    division_prices.insert(0, 0)"""

new_class = """    division_prices_data = get_division_prices()
    division_prices = (
        [item for sublist in division_prices_data for item in sublist if isinstance(sublist, (list, tuple))]
        if division_prices_data and isinstance(division_prices_data, (list, tuple))
        else []
    )
    division_prices.insert(0, 0)"""

content = content.replace(old_class, new_class)

# Write the file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed order_information.py")
PYFIX

echo ""
echo "✅ Files fixed successfully!"
echo ""
echo "🔄 Rebuilding Docker containers..."
docker-compose -f docker-compose.prod.yml build --no-cache web

echo "🚀 Restarting web container..."
docker-compose -f docker-compose.prod.yml up -d web

echo ""
echo "✅ All fixes applied! Check logs with:"
echo "   docker-compose -f docker-compose.prod.yml logs --tail=100 web"
echo ""
echo "Test the application:"
echo "   curl -I http://127.0.0.1:8000"
