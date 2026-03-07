from django.urls import path
from .views import *

app_name = 'parent_app'

urlpatterns = [
    path('search-parent/', search_parent, name='search_parent'),
    path('add/', add_parent, name='add_parent'),
]