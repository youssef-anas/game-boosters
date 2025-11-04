from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    # Main Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('test/', views.TestDashboardView.as_view(), name='test_dashboard'),
    
    # Accounts Management
    path('accounts/', views.AccountsView.as_view(), name='accounts'),
    path('accounts/boosters/', views.BoosterAccountsView.as_view(), name='booster_accounts'),
    path('accounts/clients/', views.ClientAccountsView.as_view(), name='client_accounts'),
    path('accounts/managers/', views.ManagerAccountsView.as_view(), name='manager_accounts'),
    path('force-logout/', views.AdminForceLogoutView.as_view(), name='force_logout'),
    
    # Transactions
    path('transactions/', views.TransactionsView.as_view(), name='transactions'),
    path('transactions/analytics/', views.TransactionAnalyticsView.as_view(), name='transaction_analytics'),
    
    # Pricing and Promo Codes
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('promo-codes/', views.PromoCodeView.as_view(), name='promo_codes'),
    path('api/promo/', views.PromoAPI.as_view(), name='api_promo'),
    # Pricing APIs
    path('api/pricing/<str:game_key>/', views.PricingDataAPI.as_view(), name='api_pricing_data'),
    path('api/update-price/', views.UpdatePriceAPI.as_view(), name='api_update_price'),
    path('api/bulk-update-prices/', views.BulkUpdatePricesAPI.as_view(), name='api_bulk_update_prices'),
    
    # Chat Monitoring
    path('chat/', views.ChatMonitorView.as_view(), name='chat_monitor'),
    path('chat/client-booster/', views.ClientBoosterChatView.as_view(), name='client_booster_chat'),
    path('chat/manager-booster/', views.ManagerBoosterChatView.as_view(), name='manager_booster_chat'),
    
    # Analytics and Reports
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    
    # API Endpoints
    path('api/updates/', views.AdminUpdatesAPI.as_view(), name='api_updates'),
    path('api/search/', views.SearchAPI.as_view(), name='api_search'),
    path('api/delete/<str:model>/<int:pk>/', views.DeleteAPI.as_view(), name='api_delete'),
    
    # Booster Management API
    path('api/booster/<int:booster_id>/', views.BoosterDetailAPI.as_view(), name='api_booster_detail'),
    path('api/booster/commission/', views.BoosterCommissionAPI.as_view(), name='api_booster_commission'),
    path('api/booster/<int:booster_id>/delete/', views.BoosterDeleteAPI.as_view(), name='api_booster_delete'),
    path('api/booster/comment/', views.BoosterCommentAPI.as_view(), name='api_booster_comment'),

    # Client Management API
    path('api/client/<int:client_id>/', views.ClientDetailAPI.as_view(), name='api_client_detail'),
    path('api/client/<int:client_id>/delete/', views.ClientDeleteAPI.as_view(), name='api_client_delete'),

    # Manager Management API
    path('api/manager/add/', views.ManagerAddAPI.as_view(), name='api_manager_add'),
    path('api/manager/<int:manager_id>/', views.ManagerDetailAPI.as_view(), name='api_manager_detail'),
    path('api/manager/<int:manager_id>/delete/', views.ManagerDeleteAPI.as_view(), name='api_manager_delete'),
    path('api/manager/comment/', views.ManagerCommentAPI.as_view(), name='api_manager_comment'),
    path('api/manager/password/', views.ManagerPasswordAPI.as_view(), name='api_manager_password'),

    # Transactions APIs
    path('api/transaction/<int:transaction_id>/', views.TransactionDetailAPI.as_view(), name='api_transaction_detail'),
    path('api/order/<int:order_id>/', views.OrderDetailAPI.as_view(), name='api_order_detail'),
    path('api/refund/', views.RefundAPI.as_view(), name='api_refund'),
] 