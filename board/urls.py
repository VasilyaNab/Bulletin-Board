from django.urls import path
from .views import announcement_list, profile
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

app_name = 'board'

urlpatterns = [
    path('', announcement_list, name='announcement_list'),
    path('logout/', 
         LogoutView.as_view(template_name = 'logout.html'),
         name='logout'),
    path('profile/', profile, name='profile'),
]