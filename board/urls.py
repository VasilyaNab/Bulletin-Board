from django.urls import path
from .views import (
    profile,
    response_list,
    response_action,
    announcement_list,
    announcement_detail,
    create_response,
    newsletter_view,
    AnnouncementCreateView,
    AnnouncementUpdateView,
    AnnouncementDeleteView
)
from django.contrib.auth.views import LogoutView

app_name = 'board'

urlpatterns = [
    path('', announcement_list, name='announcement_list'),
    path('announcement/<int:pk>/', announcement_detail, name='announcement-detail'),
    path('announcement/create/', AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcement/<int:pk>/edit/', AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/responses/', response_list, name='response-list'),
    path('profile/responses/<int:pk>/<str:action>/', response_action, name='response-action'),
    path('announcement/<int:announcement_id>/create-response/', create_response, name='create-response'),
    path('newsletter/', newsletter_view, name='newsletter'),
]