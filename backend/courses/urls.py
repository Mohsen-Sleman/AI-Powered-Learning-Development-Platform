from django.urls import include,path
from .views import RetriveCourse

urlpatterns = [
    path('course/<slug:slug>',RetriveCourse.as_view(),name = 'course')
]
