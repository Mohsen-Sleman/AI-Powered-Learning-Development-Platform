from django.urls import path
from users.views import RegisterView,LogoutView,ProfileView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileView.as_view(),name='update-profile'),
    path('logout/',LogoutView.as_view(),name='logout'),
]
