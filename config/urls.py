from django.contrib import admin
from django.urls import include, path
from apps.tickets import views as ticket_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', ticket_views.dashboard, name='dashboard'),
    path('profile/', include('apps.accounts.urls')),
    path('assets/', include('apps.assets.urls')),
    path('tickets/', include('apps.tickets.urls')),
]
