from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('add_photo/', views.add_photo, name='add_photo'),
    path('gallery/', views.gallery, name='gallery'),
    path('add_event/', views.add_event, name='add_event'),
    path('events/', views.events, name='events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
]