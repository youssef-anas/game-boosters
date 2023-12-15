from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from gameBoosterss.views import index

urlpatterns = [
    path('', index, name="homepage.index"),
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('booster/', include('booster.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('wildRift/', include('wildRift.urls'), name='wildRift'),
    path('accounts/', include('accounts.urls')),
    path('paypal/', include("paypal.standard.ipn.urls")),
    path('chats/', include('chat.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)