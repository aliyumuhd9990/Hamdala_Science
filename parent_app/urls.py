from django.urls import path
from .views import add_parent

app_name = 'parent_app'

urlpatterns = [
    path('add/', add_parent, name='add_parent'),
]