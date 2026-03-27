from django.urls import include,path
from .views import RetriveCourse,CreateUserEnrollment,ListUserEnrollment,ProgressEnrollmentUpdateApiView,CourseListView

urlpatterns = [
    path('courses/<slug:slug>/',RetriveCourse.as_view(),name = 'course'),
    path('courses/',CourseListView.as_view(),name="courses"),
    path('enroll/',CreateUserEnrollment.as_view(),name= 'create-user-enroll'),
    path('enrollments/',ListUserEnrollment.as_view(),name= 'list-user-enrollments'),
    path('courses/<slug:slug>/progress/',ProgressEnrollmentUpdateApiView.as_view() , name = 'update-progress-enrollment'),
]
