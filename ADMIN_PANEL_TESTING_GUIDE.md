# 🎯 Admin Panel Testing Guide

## 📍 How to Access the Admin Panel

### 1. **Create Superuser** (if not already created)
```bash
# On your VPS
cd /opt/game-boosters
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

Enter:
- **Username**: `admin` (or your choice)
- **Email**: `admin@madboost.gg` (optional)
- **Password**: `YourSecurePassword123!` (or your choice)

### 2. **Access Admin Panel**
- **URL**: `http://46.202.131.43/admin/` (or `https://madboost.gg/admin/` when SSL is ready)
- **Login**: Use your superuser credentials

---

## 🎨 Admin Panel Features Overview

### ✅ **1. Main Dashboard** (`/admin/dashboard/`)

**What You'll See:**
- **Total Revenue**: Sum of all completed transactions
- **Active Orders**: Pending orders count
- **Active Boosters**: Number of active boosters
- **Total Clients**: Number of customer accounts
- **Revenue Analytics**: Chart showing revenue over time (Today, Week, Month)
- **Recent Orders**: Last 5 orders
- **Recent Transactions**: Last 5 transactions
- **Active Chats**: Number of active chat rooms

**Quick Links Section:**
- Boosters Management
- Clients Management
- Managers Management
- Transactions
- Chat Monitor
- Pricing Management
- Promo Codes
- Test Realtime Sync
- Test Notifications

---

### ✅ **2. Account Management**

#### **A. Boosters Management** (`/admin/dashboard/accounts/boosters/`)

**Features:**
- **List View**: All boosters with pagination (20 per page)
- **Search**: Search by username or email
- **Filter by Game**: Filter boosters by game specialization
- **Sort Options**: Sort by ongoing orders, completed orders, or earnings
- **Statistics**:
  - Total boosters
  - Active boosters
  - Total earnings (all boosters combined)
  - Average rating
  - Game breakdown (boosters per game)

**Booster Details (via API):**
- Username, Email, Discord ID, PayPal account
- Ongoing orders count
- Completed orders count
- Lifetime earnings
- Average rating
- Games they specialize in
- Admin comments
- Commission rate

**Actions Available:**
- View booster details
- Add admin comments
- Set commission rate
- Delete booster (via API)

#### **B. Clients Management** (`/admin/dashboard/accounts/clients/`)

**Features:**
- **List View**: All client accounts with pagination
- **Search**: Search by username or email
- **Statistics**:
  - Total clients
  - Active clients
  - Total spent (all clients)
  - Average order value

**Client Details (via API):**
- Username, Email
- Total spent
- All orders (with game, type, price, status, date)
- Ongoing orders count
- Completed orders count
- Last order details

**Actions Available:**
- View client details
- Delete client account (via API)

#### **C. Managers Management** (`/admin/dashboard/accounts/managers/`)

**Features:**
- **List View**: All manager accounts (staff users)
- **Statistics**:
  - Total managers
  - Active managers

**Manager Details (via API):**
- Username, Email
- Last online time
- Messages sent (last 24h, last 7 days)
- Rooms active in (last 24h)
- Recent messages
- Admin comments

**Actions Available:**
- Create new manager (via API)
- View manager details
- Add admin comments
- Reset password (via API)
- Delete manager (via API)

---

### ✅ **3. Transactions Management** (`/admin/dashboard/transactions/`)

**Features:**
- **List View**: All transactions with pagination
- **Filters**:
  - Date range (from/to)
  - Status (New, Continue, Done, Drop)
  - Type (DEPOSIT, WITHDRAWAL)
- **Statistics**:
  - Total transactions
  - Total revenue
  - Today's revenue
  - Week's revenue
  - Month's revenue

**Transaction Details (via API):**
- Amount, Status, Payment method
- User information (username, email, total spent)
- Order information (if linked)
- Created date

**Actions Available:**
- View transaction details
- Process refunds (via API)
- Filter and search transactions

---

### ✅ **4. Chat Monitoring** (`/admin/dashboard/chat/`)

**Features:**
- **Statistics**:
  - Total chats (unique rooms)
  - Active chats (last hour)
  - Total messages
  - Recent messages (last 10)

**Sub-sections:**
- **Client-Booster Chat**: Monitor client-booster conversations
- **Manager-Booster Chat**: Monitor manager-booster conversations

---

### ✅ **5. Pricing Management** (`/admin/dashboard/pricing/`)

**Features:**
- **Game-based Pricing**: Manage prices for different games
- **API Endpoints**:
  - Get pricing data for a game: `/admin/dashboard/api/pricing/<game_key>/`
  - Update single price: `/admin/dashboard/api/update-price/`
  - Bulk update prices: `/admin/dashboard/api/bulk-update-prices/`

**What You Can Do:**
- View pricing for each game
- Update individual service prices
- Bulk update multiple prices at once
- Set service names and descriptions

---

### ✅ **6. Promo Codes Management** (`/admin/dashboard/promo-codes/`)

**Features:**
- **List View**: All promo codes (last 50)
- **Statistics**: Total promo codes count

**Actions Available (via API):**
- **Create Promo Code**:
  - Code (auto-generated if not provided)
  - Description
  - Discount amount
  - Is percentage (True/False)
  - Days valid (default: 30)
- **Delete Promo Code**: Remove promo code by code

**Promo Code Fields:**
- Code (unique identifier)
- Description
- Discount amount
- Is percentage (True/False)
- Expiration date
- Is active (True/False)
- Created date

---

### ✅ **7. Analytics & Reports**

**Analytics View** (`/admin/dashboard/analytics/`):
- Total orders
- Total revenue
- Revenue trends

**Reports View** (`/admin/dashboard/reports/`):
- Available reports: Orders, Revenue, Users, Boosters

---

## 🔧 Changes Made to Admin Panel

### ✅ **1. Added `admin_dashboard` App**

**What Was Added:**
- New Django app: `admin_dashboard`
- Added to `INSTALLED_APPS` in `settings.py`
- Custom admin dashboard views and templates

### ✅ **2. New Models Created**

**A. `BoosterComment`**:
- Store admin comments for boosters
- Fields: booster, admin, comment, created_at, updated_at

**B. `BoosterCommission`**:
- Store booster commission rates
- Fields: booster, percentage, notes, set_by, created_at, is_active

**C. `ManagerComment`**:
- Store admin comments for managers
- Fields: manager, admin, comment, created_at, updated_at

**D. `PricingEntry`**:
- Store game-specific pricing data
- Fields: game_key, service_id, name, description, price, updated_at

### ✅ **3. New Views & URLs**

**Main Views:**
- `DashboardView`: Main dashboard with statistics
- `AccountsView`: Account management overview
- `BoosterAccountsView`: Booster management
- `ClientAccountsView`: Client management
- `ManagerAccountsView`: Manager management
- `TransactionsView`: Transaction monitoring
- `ChatMonitorView`: Chat monitoring
- `PricingView`: Pricing management
- `PromoCodeView`: Promo code management
- `AnalyticsView`: Analytics dashboard
- `ReportsView`: Reports generation

**API Views:**
- `BoosterDetailAPI`: Get booster details
- `BoosterCommentAPI`: Add comments to boosters
- `BoosterCommissionAPI`: Set commission rates
- `BoosterDeleteAPI`: Delete booster
- `ClientDetailAPI`: Get client details
- `ClientDeleteAPI`: Delete client
- `ManagerAddAPI`: Create manager
- `ManagerDetailAPI`: Get manager details
- `ManagerCommentAPI`: Add comments to managers
- `ManagerPasswordAPI`: Reset manager password
- `ManagerDeleteAPI`: Delete manager
- `TransactionDetailAPI`: Get transaction details
- `OrderDetailAPI`: Get order details
- `RefundAPI`: Process refunds
- `PromoAPI`: Create/delete promo codes
- `PricingDataAPI`: Get pricing data
- `UpdatePriceAPI`: Update single price
- `BulkUpdatePricesAPI`: Bulk update prices

### ✅ **4. Admin Panel Integration**

**URL Configuration:**
- Added `/admin/dashboard/` route before Django admin
- All dashboard URLs are under `/admin/dashboard/`

**Django Admin Integration:**
- `BoosterComment` and `BoosterCommission` registered in Django admin
- Custom admin classes with list display, filters, and search

### ✅ **5. Security & Permissions**

**Access Control:**
- All views require `AdminRequiredMixin`
- Checks: `is_staff` or `is_superuser`
- Managers get baseline view permissions for key models

**API Security:**
- CSRF exempt for API endpoints (using `@csrf_exempt`)
- All APIs require admin authentication

---

## 🧪 Testing Checklist

### ✅ **1. Login & Access**
- [ ] Can log in with superuser credentials
- [ ] Can access `/admin/` (Django admin)
- [ ] Can access `/admin/dashboard/` (Custom dashboard)

### ✅ **2. Main Dashboard**
- [ ] Statistics display correctly (revenue, orders, boosters, clients)
- [ ] Revenue chart displays (if data exists)
- [ ] Recent orders list shows
- [ ] Recent transactions list shows
- [ ] Quick links work

### ✅ **3. Boosters Management**
- [ ] Can view list of boosters
- [ ] Can search boosters
- [ ] Can filter by game
- [ ] Can sort by different criteria
- [ ] Can view booster details (via API)
- [ ] Can add comments to boosters
- [ ] Can set commission rates

### ✅ **4. Clients Management**
- [ ] Can view list of clients
- [ ] Can search clients
- [ ] Can view client details (via API)
- [ ] Can see client orders and spending

### ✅ **5. Managers Management**
- [ ] Can view list of managers
- [ ] Can create new manager (via API)
- [ ] Can view manager details (via API)
- [ ] Can add comments to managers
- [ ] Can reset manager password

### ✅ **6. Transactions**
- [ ] Can view list of transactions
- [ ] Can filter by date range
- [ ] Can filter by status
- [ ] Can filter by type
- [ ] Can view transaction details
- [ ] Can process refunds (via API)

### ✅ **7. Chat Monitoring**
- [ ] Can view chat statistics
- [ ] Can see recent messages
- [ ] Can monitor active chats

### ✅ **8. Pricing Management**
- [ ] Can view pricing for games
- [ ] Can update prices (via API)
- [ ] Can bulk update prices (via API)

### ✅ **9. Promo Codes**
- [ ] Can view list of promo codes
- [ ] Can create promo codes (via API)
- [ ] Can delete promo codes (via API)

---

## 🔍 What to Test Specifically

### **1. CSGO2 Price Functions** (Your Request)
Since you mentioned testing CSGO2 price functions:

**Test These:**
1. **Access Pricing Page**: `/admin/dashboard/pricing/`
2. **Get CSGO2 Prices**: `/admin/dashboard/api/pricing/csgo2/`
3. **Update CSGO2 Prices**: Use the update price API
4. **Verify in Game**: Check if prices reflect in CSGO2 order forms

**Expected Behavior:**
- Prices should load without errors
- No `IndexError` when accessing price arrays
- No `NoneType` errors when no data exists
- Default values (zeros) should be returned if no data

### **2. Dashboard Statistics**
- Verify all counts are accurate
- Check revenue calculations
- Verify order status counts

### **3. API Endpoints**
- Test all API endpoints with proper authentication
- Verify error handling for invalid requests
- Check JSON responses are valid

---

## 🐛 Common Issues & Solutions

### **Issue 1: "admin_dashboard not in INSTALLED_APPS"**
**Solution**: Ensure `admin_dashboard.apps.AdminDashboardConfig` is in `INSTALLED_APPS`

### **Issue 2: "Template not found"**
**Solution**: Ensure templates are in `admin_dashboard/templates/admin_dashboard/`

### **Issue 3: "Permission denied"**
**Solution**: Ensure user has `is_staff=True` or `is_superuser=True`

### **Issue 4: "API returns 403"**
**Solution**: Ensure user is logged in and has admin privileges

---

## 📊 Expected Data Display

### **If Database is Empty:**
- Statistics will show `0` for counts
- Revenue will show `$0.00`
- Lists will be empty
- Charts may not display (no data)

### **If Database Has Data:**
- All statistics should reflect actual data
- Lists should show paginated results
- Charts should display with data
- Recent items should show latest entries

---

## 🎯 Quick Test Commands

```bash
# On VPS - Check if admin_dashboard is accessible
curl -I http://127.0.0.1:8000/admin/dashboard/

# Test API endpoint (requires authentication)
curl -X GET http://127.0.0.1:8000/admin/dashboard/api/pricing/csgo2/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID"

# Check container logs for errors
docker-compose -f docker-compose.prod.yml logs web | grep -i error
```

---

## 📝 Notes

- **All dashboard features require admin authentication**
- **API endpoints use JSON responses**
- **Some features require existing data to display properly**
- **Charts use Chart.js library (loaded via CDN)**
- **All views extend Django admin base template**

---

**Last Updated**: November 2024
**Status**: ✅ Ready for Testing

