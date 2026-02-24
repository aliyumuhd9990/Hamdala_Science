from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core_app.urls', namespace="core_app")),
    path('accounts/', include('accounts.urls')),
]
