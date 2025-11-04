from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def realtime_test(request):
    """
    View for testing real-time WebSocket synchronization.
    """
    # Get the host from request
    host = request.get_host()
    # Remove port if using standard ports (80 for http, 443 for https)
    if ':8000' in host:
        # For development, keep the port
        pass
    elif ':80' in host:
        host = host.replace(':80', '')
    elif ':443' in host:
        host = host.replace(':443', '')
    
    context = {
        'ws_host': host,
        'ws_protocol': 'wss' if request.is_secure() else 'ws',
    }
    return render(request, 'realtime/realtime_test.html', context)

