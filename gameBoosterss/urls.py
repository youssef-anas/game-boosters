from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from gameBoosterss.views import index, last_orders, privacy_policy, terms_service, download_media_zip, social_auth_exception_handler, facebook_data_deletion_handler, StoreView, HowWeWorkView
from django.conf.urls import handler400, handler403, handler404, handler500
# from oauth2_provider import views as oauth2_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', index, name="homepage.index"),
    path('last_orders/', last_orders, name="last.orders"),
    path('privacy-policy/', privacy_policy, name='privacy.policy'),
    path('terms-service/', terms_service, name='terms.service'),
    path('social-auth-exception/', social_auth_exception_handler, name='social_auth_exception_handler'),
    path('facebook-data-deletion/', facebook_data_deletion_handler, name='facebook_data_deletion'),
    path('rmtp9o0h7ntmxakmat8fpe2zhuj9by.html', TemplateView.as_view(template_name='rmtp9o0h7ntmxakmat8fpe2zhuj9by.html'), name='html_verification'),
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('booster/', include('booster.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('wildRift/', include('wildRift.urls')),
    path('accounts/', include('accounts.urls')),
    path('valorant/', include('valorant.urls')),
    path('lol/', include('leagueOfLegends.urls')),
    path('pubg/', include('pubg.urls')),
    path('wow/', include('WorldOfWarcraft.urls')),
    path('tft/', include('tft.urls')),
    path('hearthstone/', include('hearthstone.urls')),
    path('rocketLeague/', include('rocketLeague.urls')),
    path('mobileLegends/', include('mobileLegends.urls')),
    path('dota2/', include('dota2.urls')),
    path('overwatch2/', include('overwatch2.urls')),
    path('csgo2/', include('csgo2.urls')),
    path('hok/', include('honorOfKings.urls')),
    path('games/', include('games.urls')),
    path('chat/', include('chat.urls')),
    # path('paypal/', include("paypal.standard.ipn.urls")),
    # path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    # path('token/', oauth2_views.TokenView.as_view(), name="token"),
    # path('accounts/', include('allauth.urls')),
    path('download/media/zip/', download_media_zip, name='download_media_zip'),
    path('social/', include('social_django.urls', namespace='social')),

    path('store/',StoreView.as_view(), name='store'),

    path('blog/', include('news.urls')),
    path('how-we-work/', HowWeWorkView.as_view(), name='how-we-work'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = 'gameBoosterss.views.custom_handler400'
handler403 = 'gameBoosterss.views.custom_handler403'
handler404 = 'gameBoosterss.views.custom_handler404'
handler500 = 'gameBoosterss.views.custom_handler500'


# Customizing the default Django admin site titles
admin.site.site_header = "Madboost Admin"  # Sets the text on the top of the admin site
admin.site.site_title = "Madboost Admin"   # Sets the text shown on the browser tab
admin.site.index_title = "Admin"  