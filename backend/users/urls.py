from django.urls import path,include
from users.views import RegisterView,LogoutView,ProfileView,GoogleLogin,GitHubLogin,VerifyOTPView,ResendOTPView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/update/',ProfileView.as_view(),name='update-profile'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('github/', GitHubLogin.as_view(), name='github_login'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
]
