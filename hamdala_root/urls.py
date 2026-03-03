from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core_app.urls', namespace="core_app")),
    path('accounts/', include('accounts.urls')),
    path('principal/', include('principal_app.urls', namespace="principal_app")),
    path('student/', include('student_app.urls', namespace="student_app")),
    path('parents/', include('parent_app.urls', namespace="parent_app")),
]
