from django.urls import path
from . import views

urlpatterns = [
    path('cms/', views.cms_view, name='cms'),
]
