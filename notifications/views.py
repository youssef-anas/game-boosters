from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def test_notifications(request):
    # Infer a simple role for demo; admins -> admin, boosters -> booster, default customer
    role = 'customer'
    user = request.user
    if getattr(user, 'is_superuser', False):
        role = 'admin'
    elif getattr(user, 'is_booster', False):
        role = 'booster'
    return render(request, 'notifications/test_notifications.html', {
        'role': role,
        'ws_protocol': 'wss' if request.is_secure() else 'ws',
        'host': request.get_host(),
    })



