from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, Q, Avg
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import Permission, ContentType

# Import your models
from accounts.models import BaseUser, BaseOrder, Transaction, Wallet
from booster.models import Booster, OrderRating
from chat.models import Message
from admin_dashboard.models import BoosterComment, BoosterCommission, ManagerComment
from games.models import Game
from .models import PricingEntry

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure user has admin privileges"""
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class DashboardView(AdminRequiredMixin, TemplateView):
    """Main admin dashboard with overview widgets"""
    template_name = 'admin_dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current date and time ranges
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Dashboard statistics
        context.update({
            'total_boosters': Booster.objects.count(),
            'active_boosters': Booster.objects.count(),  # All boosters are considered active
            'total_clients': BaseUser.objects.filter(is_customer=True).count(),
            'total_orders': BaseOrder.objects.count(),
            'pending_orders': BaseOrder.objects.filter(status='New').count(),
            'completed_orders': BaseOrder.objects.filter(status='Done').count(),
            'total_revenue': Transaction.objects.filter(status='Done').aggregate(Sum('amount'))['amount__sum'] or 0,
            
            # Time-based statistics
            'today_revenue': Transaction.objects.filter(
                status='Done',
                date__date=today
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            
            'week_revenue': Transaction.objects.filter(
                status='Done',
                date__date__gte=week_ago
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            
            'month_revenue': Transaction.objects.filter(
                status='Done',
                date__date__gte=month_ago
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            
            # Recent activity
            'recent_orders': BaseOrder.objects.order_by('-created_at')[:5],
            'recent_transactions': Transaction.objects.order_by('-date')[:5],
            'active_chats': Message.objects.filter(
                created_on__gte=now - timedelta(hours=1)
            ).values('room').distinct().count(),
        })
        
        return context

# Manager Management APIs
@method_decorator(csrf_exempt, name='dispatch')
class ManagerAddAPI(AdminRequiredMixin, TemplateView):
    """Create a new manager (is_staff=True)"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            supplied_password = data.get('password')
            password = supplied_password or BaseUser.objects.make_random_password()
            if not username or not email:
                return JsonResponse({'error': 'username and email are required'}, status=400)
            if BaseUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'username already exists'}, status=400)
            user = BaseUser.objects.create_user(username=username, email=email, password=password)
            user.is_staff = True
            user.is_customer = False
            user.is_booster = False
            user.save()

            # Grant baseline view permissions so managers can see data in Django admin
            try:
                baseline_models = [
                    ('accounts', 'baseuser'),
                    ('accounts', 'baseorder'),
                    ('accounts', 'transaction'),
                    ('booster', 'booster'),
                    ('chat', 'message'),
                ]
                codenames = []
                for app_label, model in baseline_models:
                    ct = ContentType.objects.get(app_label=app_label, model=model)
                    perm = Permission.objects.get(content_type=ct, codename=f"view_{model}")
                    codenames.append(perm)
                user.user_permissions.add(*codenames)
            except Exception:
                # If any permission is missing, skip gracefully; custom dashboard still works
                pass
            return JsonResponse({'success': True, 'id': user.id, 'username': user.username, 'password': password, 'auto_password': supplied_password is None or supplied_password == ''})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ManagerDetailAPI(AdminRequiredMixin, TemplateView):
    """Get manager details: activity, comments, recent messages"""
    def get(self, request, manager_id):
        try:
            mgr = get_object_or_404(BaseUser, pk=manager_id, is_staff=True)
            now = timezone.now()
            day_ago = now - timedelta(days=1)
            week_ago = now - timedelta(days=7)

            msgs_24h = Message.objects.filter(user=mgr, created_on__gte=day_ago).count()
            msgs_7d = Message.objects.filter(user=mgr, created_on__gte=week_ago).count()
            rooms_24h = Message.objects.filter(user=mgr, created_on__gte=day_ago).values('room').distinct().count()
            recent_msgs = list(Message.objects.filter(user=mgr).order_by('-created_on').values('content', 'created_on')[:10])

            comments = ManagerComment.objects.filter(manager=mgr).order_by('-created_at')[:10]
            comments_data = [{
                'id': c.id,
                'comment': c.comment,
                'admin': c.admin.username,
                'created_at': c.created_at.strftime('%Y-%m-%d %H:%M'),
            } for c in comments]

            data = {
                'id': mgr.id,
                'username': mgr.username,
                'email': mgr.email,
                'is_active': mgr.is_active,
                'last_online': mgr.last_online.strftime('%Y-%m-%d %H:%M') if mgr.last_online else None,
                'messages_last_24h': msgs_24h,
                'messages_last_7d': msgs_7d,
                'rooms_last_24h': rooms_24h,
                'recent_messages': [{'content': m['content'], 'created_at': m['created_on'].strftime('%Y-%m-%d %H:%M') if m['created_on'] else None} for m in recent_msgs],
                'comments': comments_data,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ManagerDeleteAPI(AdminRequiredMixin, TemplateView):
    """Delete a manager account (cannot delete superusers)"""
    def delete(self, request, manager_id):
        try:
            mgr = get_object_or_404(BaseUser, pk=manager_id, is_staff=True)
            if mgr.is_superuser:
                return JsonResponse({'error': 'Cannot delete superuser'}, status=400)
            username = mgr.username
            mgr.delete()
            return JsonResponse({'success': True, 'message': f'Manager {username} deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ManagerCommentAPI(AdminRequiredMixin, TemplateView):
    """Add an admin comment on a manager"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            manager_id = data.get('manager_id')
            comment_text = data.get('comment')
            if not comment_text or not manager_id:
                return JsonResponse({'error': 'manager_id and comment are required'}, status=400)
            mgr = get_object_or_404(BaseUser, pk=manager_id, is_staff=True)
            ManagerComment.objects.create(manager=mgr, admin=request.user, comment=comment_text.strip())
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ManagerPasswordAPI(AdminRequiredMixin, TemplateView):
    """Set or reset a manager password"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            manager_id = data.get('manager_id')
            new_password = data.get('password') or BaseUser.objects.make_random_password()
            mgr = get_object_or_404(BaseUser, pk=manager_id, is_staff=True)
            mgr.set_password(new_password)
            mgr.save(update_fields=['password'])
            return JsonResponse({'success': True, 'password': new_password})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ClientDetailAPI(AdminRequiredMixin, TemplateView):
    """API endpoint to get client details: totals, orders, ongoing"""
    
    def get(self, request, client_id):
        try:
            client = get_object_or_404(BaseUser, pk=client_id, is_customer=True)
            total_spent = Transaction.objects.filter(user=client, status='Done').aggregate(Sum('amount'))['amount__sum'] or 0
            orders_qs = BaseOrder.objects.filter(customer=client).select_related('game').order_by('-created_at')
            ongoing_count = orders_qs.filter(status__in=['New', 'Continue']).count()
            completed_count = orders_qs.filter(status='Done').count()
            last_order = orders_qs.first()
            orders_data = [{
                'id': o.id,
                'game': o.game.name if o.game else None,
                'type': o.game_type,
                'price': o.price,
                'status': o.status,
                'created_at': o.created_at.strftime('%Y-%m-%d %H:%M') if o.created_at else None,
            } for o in orders_qs[:20]]
            data = {
                'id': client.id,
                'username': client.username,
                'email': client.email,
                'is_active': client.is_active,
                'total_spent': float(total_spent),
                'orders': orders_data,
                'ongoing_orders': ongoing_count,
                'completed_orders': completed_count,
                'last_order': {
                    'id': last_order.id,
                    'price': last_order.price,
                    'status': last_order.status,
                    'created_at': last_order.created_at.strftime('%Y-%m-%d %H:%M') if last_order and last_order.created_at else None,
                } if last_order else None,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ClientDeleteAPI(AdminRequiredMixin, TemplateView):
    """API endpoint to delete a client account"""
    
    def delete(self, request, client_id):
        try:
            client = get_object_or_404(BaseUser, pk=client_id, is_customer=True)
            username = client.username
            client.delete()
            return JsonResponse({'success': True, 'message': f'Client {username} deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

class TestDashboardView(AdminRequiredMixin, TemplateView):
    """Simple test dashboard to debug issues"""
    template_name = 'admin_dashboard/test_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current date and time ranges
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Dashboard statistics
        context.update({
            'total_boosters': Booster.objects.count(),
            'active_boosters': Booster.objects.count(),
            'total_clients': BaseUser.objects.filter(is_customer=True).count(),
            'total_orders': BaseOrder.objects.count(),
            'pending_orders': BaseOrder.objects.filter(status='New').count(),
            'completed_orders': BaseOrder.objects.filter(status='Done').count(),
            'total_revenue': Transaction.objects.filter(status='Done').aggregate(Sum('amount'))['amount__sum'] or 0,
        })
        
        return context

class AccountsView(AdminRequiredMixin, TemplateView):
    """Accounts management overview"""
    template_name = 'admin_dashboard/accounts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Account statistics
        context.update({
            'total_users': BaseUser.objects.count(),
            'total_boosters': Booster.objects.count(),
            'total_clients': BaseUser.objects.filter(is_customer=True).count(),
            'total_managers': BaseUser.objects.filter(is_staff=True).count(),
            
            # Account status breakdown
            'active_accounts': BaseUser.objects.filter(is_active=True).count(),
            'inactive_accounts': BaseUser.objects.filter(is_active=False).count(),
        })
        
        return context

class AdminForceLogoutView(AdminRequiredMixin, TemplateView):
    """Admin-only helper endpoint to perform logout via GET and redirect to admin login."""
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/admin/login/?next=/admin/')

@method_decorator(csrf_exempt, name='dispatch')
class AdminLogoutOverrideView(TemplateView):
    """Override Django admin logout to allow GET and avoid CSRF issues."""
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/admin/login/?next=/admin/')
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('/admin/login/?next=/admin/')

class BoosterAccountsView(AdminRequiredMixin, ListView):
    """Booster accounts management"""
    model = Booster
    template_name = 'admin_dashboard/booster_accounts.html'
    context_object_name = 'boosters'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = (
            Booster.objects.select_related('booster')
            .prefetch_related('games')
            .annotate(
                ongoing_orders=Count(
                    'booster__booster_orders',
                    filter=Q(booster__booster_orders__status__in=['New', 'Continue']),
                    distinct=True,
                ),
                completed_orders=Count(
                    'booster__booster_orders',
                    filter=Q(booster__booster_orders__status='Done'),
                    distinct=True,
                ),
                lifetime_earnings=Sum(
                    'booster__transaction__amount',
                    filter=Q(
                        booster__transaction__type='DEPOSIT',
                        booster__transaction__status='Done',
                    ),
                    default=0.0,
                ),
            )
        )
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(booster__username__icontains=search_query) |
                Q(booster__email__icontains=search_query)
            )
        
        # Filter by game (through many-to-many to Game)
        game_filter = self.request.GET.get('game')
        if game_filter:
            queryset = queryset.filter(games__name__icontains=game_filter)
        
        # Optional sort parameter
        sort_by = self.request.GET.get('sort')
        if sort_by in ['ongoing', 'completed', 'earnings']:
            order_map = {
                'ongoing': '-ongoing_orders',
                'completed': '-completed_orders',
                'earnings': '-lifetime_earnings',
            }
            queryset = queryset.order_by(order_map[sort_by])
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate total earnings from all boosters
        total_earnings = Transaction.objects.filter(
            user__is_booster=True,
            type='DEPOSIT',
            status='Done'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Calculate average rating from OrderRating
        avg_rating = OrderRating.objects.aggregate(Avg('rate'))['rate__avg'] or 0
        
        # Booster statistics
        context.update({
            'total_boosters': Booster.objects.count(),
            'active_boosters': Booster.objects.filter(booster__is_active=True).count(),
            'total_earnings': total_earnings,
            'avg_rating': avg_rating,
            'game_breakdown': self.get_game_breakdown(),
        })
        
        return context
    
    def get_game_breakdown(self):
        """Get breakdown of boosters by game"""
        from django.db.models import Count
        return Booster.objects.values('games__name').annotate(
            count=Count('id')
        ).order_by('-count')[:5]

class ClientAccountsView(AdminRequiredMixin, ListView):
    """Client accounts management"""
    template_name = 'admin_dashboard/client_accounts.html'
    context_object_name = 'clients'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = BaseUser.objects.filter(is_customer=True)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Client statistics
        context.update({
            'total_clients': BaseUser.objects.filter(is_customer=True).count(),
            'active_clients': BaseUser.objects.filter(is_customer=True, is_active=True).count(),
            'total_spent': Transaction.objects.filter(
                user__is_customer=True,
                status='Done'
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'avg_order_value': BaseOrder.objects.filter(
                customer__is_customer=True
            ).aggregate(Avg('price'))['price__avg'] or 0,
        })
        
        return context

class ManagerAccountsView(AdminRequiredMixin, ListView):
    """Manager accounts management"""
    template_name = 'admin_dashboard/manager_accounts.html'
    context_object_name = 'managers'
    paginate_by = 20
    
    def get_queryset(self):
        return BaseUser.objects.filter(is_staff=True).exclude(is_superuser=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Manager statistics
        context.update({
            'total_managers': BaseUser.objects.filter(is_staff=True).exclude(is_superuser=True).count(),
            'active_managers': BaseUser.objects.filter(is_staff=True, is_active=True).exclude(is_superuser=True).count(),
        })
        
        return context

class TransactionsView(AdminRequiredMixin, ListView):
    """Transaction monitoring and management"""
    model = Transaction
    template_name = 'admin_dashboard/transactions.html'
    context_object_name = 'transactions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Transaction.objects.select_related('user', 'order').all()
        
        # Filter by date range
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from:
            queryset = queryset.filter(date__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__date__lte=date_to)
        
        # Filter by status (matches STATUS_CHOICES)
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        # Filter by type
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        
        return queryset.order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Transaction statistics
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        context.update({
            'total_transactions': Transaction.objects.count(),
            'total_revenue': Transaction.objects.filter(status='Done').aggregate(Sum('amount'))['amount__sum'] or 0,
            'today_revenue': Transaction.objects.filter(
                status='Done',
                date__date=today
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'week_revenue': Transaction.objects.filter(
                status='Done',
                date__date__gte=week_ago
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'month_revenue': Transaction.objects.filter(
                status='Done',
                date__date__gte=month_ago
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
        })
        
        return context

# Transactions/detail/refund APIs
@method_decorator(csrf_exempt, name='dispatch')
class TransactionDetailAPI(AdminRequiredMixin, TemplateView):
    def get(self, request, transaction_id):
        try:
            t = Transaction.objects.select_related('user', 'order').get(id=transaction_id)
            data = {
                'id': t.id,
                'amount': float(t.amount),
                'status': t.status,
                'payment_method': t.type,
                'created_at': t.date.strftime('%Y-%m-%d %H:%M'),
                'user': {
                    'id': t.user.id,
                    'username': t.user.username,
                    'email': t.user.email,
                    'total_spent': Transaction.objects.filter(user=t.user, status='Done').aggregate(Sum('amount'))['amount__sum'] or 0,
                },
            }
            if t.order:
                data['order'] = {
                    'id': t.order.id,
                    'game': t.order.game.name if t.order.game else None,
                    'service_type': t.order.game_type,
                    'status': t.order.status,
                }
            return JsonResponse(data)
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class OrderDetailAPI(AdminRequiredMixin, TemplateView):
    def get(self, request, order_id):
        try:
            o = BaseOrder.objects.select_related('game', 'customer').get(id=order_id)
            data = {
                'id': o.id,
                'game': o.game.name if o.game else None,
                'service_type': o.game_type,
                'status': o.status,
                'total_amount': float(o.price or 0),
                'customer': {
                    'id': o.customer.id if o.customer else None,
                    'username': o.customer.username if o.customer else None,
                    'email': o.customer.email if o.customer else None,
                },
                'created_at': o.created_at.strftime('%Y-%m-%d %H:%M') if o.created_at else None,
            }
            return JsonResponse(data)
        except BaseOrder.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class RefundAPI(AdminRequiredMixin, TemplateView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            transaction_id = data.get('transaction_id')
            amount = float(data.get('amount', 0))
            reason = data.get('reason')
            notes = data.get('notes', '')
            t = Transaction.objects.get(id=transaction_id)
            if t.status == 'Done' and amount > 0:
                # Record a negative transaction as refund and mark original as Drop
                Transaction.objects.create(
                    user=t.user,
                    amount=-abs(amount),
                    order=t.order,
                    notice=f'Refund: {reason}. {notes}'.strip(),
                    status='Done',
                    type='WITHDRAWAL'
                )
                t.status = 'Drop'
                t.save(update_fields=['status'])
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Invalid refund request'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
class ChatMonitorView(AdminRequiredMixin, TemplateView):
    """Chat monitoring dashboard"""
    template_name = 'admin_dashboard/chat_monitor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Chat statistics
        now = timezone.now()
        hour_ago = now - timedelta(hours=1)
        
        context.update({
            'total_chats': Message.objects.values('room').distinct().count(),
            'active_chats': Message.objects.filter(
                created_on__gte=hour_ago
            ).values('room').distinct().count(),
            'total_messages': Message.objects.count(),
            'recent_messages': Message.objects.select_related('user').order_by('-created_on')[:10],
        })
        
        return context

class TransactionAnalyticsView(AdminRequiredMixin, TemplateView):
    """Transaction analytics and insights"""
    template_name = 'admin_dashboard/transaction_analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Transaction analytics data
        now = timezone.now()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        context.update({
            'total_transactions': Transaction.objects.count(),
            'total_revenue': Transaction.objects.filter(status='Done').aggregate(Sum('amount'))['amount__sum'] or 0,
            'today_revenue': Transaction.objects.filter(
                status='Done',
                date__date=today
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'week_revenue': Transaction.objects.filter(
                status='Done',
                date__date__gte=week_ago
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
            'month_revenue': Transaction.objects.filter(
                status='Done',
                date__date__gte=month_ago
            ).aggregate(Sum('amount'))['amount__sum'] or 0,
        })
        
        return context

# API Views for AJAX requests
class AdminUpdatesAPI(AdminRequiredMixin, TemplateView):
    """API endpoint for real-time updates"""
    
    def get(self, request, *args, **kwargs):
        # Get recent updates
        updates = {
            'new_orders': BaseOrder.objects.filter(
                created_at__gte=timezone.now() - timedelta(minutes=5)
            ).count(),
            'new_transactions': Transaction.objects.filter(
                date__gte=timezone.now() - timedelta(minutes=5)
            ).count(),
            'active_boosters': Booster.objects.filter(is_active=True).count(),
        }
        
        return JsonResponse(updates)

class SearchAPI(AdminRequiredMixin, TemplateView):
    """API endpoint for search functionality"""
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        target = request.GET.get('target', '')
        
        if not query or len(query) < 2:
            return JsonResponse({'results': []})
        
        results = []
        
        if target == 'boosters':
            boosters = Booster.objects.filter(
                Q(booster__username__icontains=query) |
                Q(booster__email__icontains=query)
            )[:10]
            
            results = [{
                'id': booster.id,
                'username': booster.booster.username,
                'email': booster.booster.email,
                'specialization': 'N/A',  # Placeholder - no specialization field
                'rating': 'N/A',  # Placeholder - no rating field
                'status': 'Active',  # Placeholder - no status field
            } for booster in boosters]
        
        elif target == 'clients':
            clients = BaseUser.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query),
                is_customer=True
            )[:10]
            
            results = [{
                'id': client.id,
                'username': client.username,
                'email': client.email,
                'total_spent': Transaction.objects.filter(user=client, status='Done').aggregate(Sum('amount'))['amount__sum'] or 0,
            } for client in clients]
        
        return JsonResponse({'results': results})

class DeleteAPI(AdminRequiredMixin, TemplateView):
    """API endpoint for deleting items"""
    
    def delete(self, request, model, pk):
        try:
            if model == 'booster':
                item = get_object_or_404(Booster, pk=pk)
            elif model == 'client':
                item = get_object_or_404(BaseUser, pk=pk, is_customer=True)
            elif model == 'transaction':
                item = get_object_or_404(Transaction, pk=pk)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid model'})
            
            item.delete()
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}) 

class PricingView(AdminRequiredMixin, TemplateView):
    """Pricing management dashboard"""
    template_name = 'admin_dashboard/pricing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_games': Game.objects.count(),
            'active_promos': 0,
        })
        return context



class PromoCodeView(AdminRequiredMixin, TemplateView):
    """Promo code management"""
    template_name = 'admin_dashboard/promo_codes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from accounts.models import PromoCode
        context.update({
            'total_promos': PromoCode.objects.count(),
            'promos': PromoCode.objects.order_by('-created_at')[:50],
        })
        return context

@method_decorator(csrf_exempt, name='dispatch')
class PromoAPI(AdminRequiredMixin, TemplateView):
    """Create and delete promo codes"""
    def post(self, request):
        try:
            from accounts.models import PromoCode
            data = json.loads(request.body or '{}')
            code = data.get('code')
            description = data.get('description')
            amount = float(data.get('discount_amount', 0))
            is_percent = bool(data.get('is_percent'))
            days = int(data.get('days_valid', 30))
            from datetime import date, timedelta
            expiration = date.today() + timedelta(days=days)
            if not code:
                import secrets
                code = secrets.token_urlsafe(6).upper()
            promo = PromoCode.objects.create(
                code=code,
                description=description or '',
                discount_amount=amount,
                expiration_date=expiration,
                is_percent=is_percent,
                is_active=True,
            )
            return JsonResponse({'success': True, 'code': promo.code})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class PricingDataAPI(AdminRequiredMixin, TemplateView):
    """Return simple pricing data per game for the editor.
    Since pricing is game-specific across multiple apps, we expose a minimal
    JSON that the UI can edit without touching core game logic.
    """
    def get(self, request, game_key):
        # Base default rows
        defaults = {
            i: {
                'id': i,
                'name': f'Service {i}',
                'description': 'Editable price',
                'current_price': round(5 * i + 9.99, 2)
            }
            for i in range(1, 6)
        }
        # Overlay persisted entries
        persisted = PricingEntry.objects.filter(game_key=game_key)
        for p in persisted:
            if p.service_id in defaults:
                defaults[p.service_id]['current_price'] = float(p.price)
                defaults[p.service_id]['name'] = p.name or defaults[p.service_id]['name']
                if p.description:
                    defaults[p.service_id]['description'] = p.description
        services = [defaults[i] for i in sorted(defaults.keys())]
        return JsonResponse({'services': services})

@method_decorator(csrf_exempt, name='dispatch')
class UpdatePriceAPI(AdminRequiredMixin, TemplateView):
    def post(self, request):
        try:
            data = json.loads(request.body or '{}')
            game_key = data.get('game_key') or request.GET.get('game_key')
            service_id = data.get('service_id')
            new_price = data.get('new_price')
            name = data.get('name') or f"Service {service_id}"
            description = data.get('description', '')
            if not game_key:
                return JsonResponse({'success': False, 'error': 'game_key missing'}, status=400)
            if service_id is None:
                return JsonResponse({'success': False, 'error': 'service_id missing'}, status=400)
            try:
                price_val = float(new_price)
            except Exception:
                return JsonResponse({'success': False, 'error': 'invalid price'}, status=400)

            PricingEntry.objects.update_or_create(
                game_key=game_key,
                service_id=service_id,
                defaults={'price': price_val, 'name': name, 'description': description}
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class BulkUpdatePricesAPI(AdminRequiredMixin, TemplateView):
    def post(self, request):
        try:
            data = json.loads(request.body or '{}')
            game_key = data.get('game_key') or request.GET.get('game_key')
            prices = data.get('prices') or []
            if not game_key:
                return JsonResponse({'success': False, 'error': 'game_key missing'}, status=400)
            updated = 0
            for item in prices:
                service_id = item.get('service_id')
                new_price = item.get('new_price')
                name = item.get('name') or f"Service {service_id}"
                description = item.get('description', '')
                if service_id is None:
                    continue
                try:
                    price_val = float(new_price)
                except Exception:
                    continue
                PricingEntry.objects.update_or_create(
                    game_key=game_key,
                    service_id=service_id,
                    defaults={'price': price_val, 'name': name, 'description': description}
                )
                updated += 1
            return JsonResponse({'success': True, 'updated_count': updated})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    def delete(self, request):
        try:
            from accounts.models import PromoCode
            data = json.loads(request.body or '{}')
            code = data.get('code')
            if not code:
                return JsonResponse({'success': False, 'error': 'code is required'}, status=400)
            PromoCode.objects.filter(code=code).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

class AnalyticsView(AdminRequiredMixin, TemplateView):
    """Analytics dashboard"""
    template_name = 'admin_dashboard/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_orders': BaseOrder.objects.count(),
            'total_revenue': Transaction.objects.filter(status='Done').aggregate(Sum('amount'))['amount__sum'] or 0,
        })
        return context

class ReportsView(AdminRequiredMixin, TemplateView):
    """Reports generation"""
    template_name = 'admin_dashboard/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'available_reports': ['Orders', 'Revenue', 'Users', 'Boosters'],
        })
        return context

class ClientBoosterChatView(AdminRequiredMixin, TemplateView):
    """Client-Booster chat monitoring"""
    template_name = 'admin_dashboard/client_booster_chat.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'active_chats': Message.objects.values('room').distinct().count(),
        })
        return context

class ManagerBoosterChatView(AdminRequiredMixin, TemplateView):
    """Manager-Booster chat monitoring"""
    template_name = 'admin_dashboard/manager_booster_chat.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'admin_chats': Message.objects.filter(room__is_for_admins=True).values('room').distinct().count(),
        })
        return context

# API Views for Booster Management
@method_decorator(csrf_exempt, name='dispatch')
class BoosterDetailAPI(AdminRequiredMixin, TemplateView):
    """API endpoint to get booster details"""
    
    def get(self, request, booster_id):
        try:
            booster = Booster.objects.select_related('booster').prefetch_related('games').get(id=booster_id)
            
            # Get performance stats
            ongoing_orders = BaseOrder.objects.filter(
                booster=booster.booster,
                status__in=['New', 'Continue']
            ).count()
            
            completed_orders = BaseOrder.objects.filter(
                booster=booster.booster,
                status='Done'
            ).count()
            
            lifetime_earnings = Transaction.objects.filter(
                user=booster.booster,
                type='DEPOSIT',
                status='Done'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            avg_rating = OrderRating.objects.filter(
                booster=booster.booster
            ).aggregate(Avg('rate'))['rate__avg'] or 0
            
            # Get admin comments
            comments = BoosterComment.objects.filter(booster=booster.booster).order_by('-created_at')[:10]
            comments_data = []
            for comment in comments:
                comments_data.append({
                    'id': comment.id,
                    'comment': comment.comment,
                    'admin': comment.admin.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                })
            
            # Get current commission
            current_commission = BoosterCommission.objects.filter(booster=booster.booster, is_active=True).first()
            commission_data = None
            if current_commission:
                commission_data = {
                    'percentage': float(current_commission.percentage),
                    'notes': current_commission.notes,
                    'set_by': current_commission.set_by.username,
                    'created_at': current_commission.created_at.strftime('%Y-%m-%d %H:%M'),
                }
            
            data = {
                'id': booster.id,
                'username': booster.booster.username,
                'email': booster.booster.email,
                'discord_id': booster.discord_id,
                'paypal_account': booster.paypal_account,
                'is_active': booster.booster.is_active,
                'ongoing_orders': ongoing_orders,
                'completed_orders': completed_orders,
                'lifetime_earnings': float(lifetime_earnings),
                'avg_rating': float(avg_rating),
                'games': [game.name for game in booster.games.all()],
                'comments': comments_data,
                'commission': commission_data,
            }
            
            return JsonResponse(data)
        except Booster.DoesNotExist:
            return JsonResponse({'error': 'Booster not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class BoosterCommissionAPI(AdminRequiredMixin, TemplateView):
    """API endpoint to set booster commission"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            booster_id = data.get('booster_id')
            percentage = data.get('percentage')
            notes = data.get('notes', '')
            
            if not percentage or float(percentage) < 0 or float(percentage) > 100:
                return JsonResponse({'error': 'Invalid commission percentage'}, status=400)
            
            booster = Booster.objects.get(id=booster_id)
            
            # Deactivate previous commissions for this booster
            BoosterCommission.objects.filter(booster=booster.booster, is_active=True).update(is_active=False)
            
            # Create new commission record
            BoosterCommission.objects.create(
                booster=booster.booster,
                percentage=percentage,
                notes=notes,
                set_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Commission set to {percentage}% for {booster.booster.username}'
            })
        except Booster.DoesNotExist:
            return JsonResponse({'error': 'Booster not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class BoosterDeleteAPI(AdminRequiredMixin, TemplateView):
    """API endpoint to delete booster"""
    
    def delete(self, request, booster_id):
        try:
            booster = Booster.objects.get(id=booster_id)
            username = booster.booster.username
            booster.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Booster {username} deleted successfully'
            })
        except Booster.DoesNotExist:
            return JsonResponse({'error': 'Booster not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class BoosterCommentAPI(AdminRequiredMixin, TemplateView):
    """API endpoint to add admin comments for booster"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            booster_id = data.get('booster_id')
            comment_text = data.get('comment')
            
            if not comment_text or not comment_text.strip():
                return JsonResponse({'error': 'Comment cannot be empty'}, status=400)
            
            booster = Booster.objects.get(id=booster_id)
            
            # Create the comment
            BoosterComment.objects.create(
                booster=booster.booster,
                admin=request.user,
                comment=comment_text.strip()
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Comment added for {booster.booster.username}'
            })
        except Booster.DoesNotExist:
            return JsonResponse({'error': 'Booster not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 