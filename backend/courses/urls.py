from django.urls import path
from .views import (CourseDetailView,UserEnrollmentCreateView,ListUserEnrollmentView,ProgressEnrollmentUpdateView,CourseListView,
                    CourseCreateView,SectionCreateView,LessonCreateView,CourseUpdateView,CourseDeleteView,
                    SectionUpdateView,SectionDeleteView,LessonUpdateView,LessonDeleteView,
                    TrackListView,TrackDetailView,TrackCreateView,TrackUpdateView,TrackDeleteView,
                    LessonDetailView,UserEnrollmentTrackCreateView,ListUserTrackEnrollmentView,
                    TrackCourseViewSet)
from rest_framework.routers import DefaultRouter
urlpatterns = [

    # Enrollments
    path('courses/enroll/',UserEnrollmentCreateView.as_view(),name= 'create-user-course-enroll'),
    path('tracks/enroll/',UserEnrollmentTrackCreateView.as_view(),name= 'create-user-track-enroll'),
    path('courses/enrollments/',ListUserEnrollmentView.as_view(),name= 'list-user-courses-enrollments'),
    path('courses/enrollments/<int:pk>/delete/',UserEnrollmentCreateView.as_view(),name= 'delete-user-course-enrollment'),
    path('tracks/enrollments/',ListUserTrackEnrollmentView.as_view(),name= 'list-user-tracks-enrollments'),
    path('tracks/enrollments/<int:pk>/delete/',UserEnrollmentTrackCreateView.as_view(),name= 'delete-user-track-enrollment'),
    path('courses/<slug:slug>/enrollment/progress/',ProgressEnrollmentUpdateView.as_view() , name = 'update-progress-enrollment'),

    # Tracks
    path('tracks/',TrackListView.as_view(),name='list-tracks'), 
    path('tracks/create/',TrackCreateView.as_view(),name='create-track'),
    path('tracks/<int:track_id>/',TrackDetailView.as_view(),name='details-track'),
    path('tracks/<int:track_id>/update/',TrackUpdateView.as_view(),name='update-track'),
    path('tracks/<int:track_id>/delete/',TrackDeleteView.as_view(),name='delete-track'),

    # Courses
    path('courses/',CourseListView.as_view(),name="list-courses"),
    path('courses/create/',CourseCreateView.as_view(),name='create-course'),
    path('courses/<slug:slug>/',CourseDetailView.as_view(),name = 'details-course'),
    path('courses/<slug:slug>/update/',CourseUpdateView.as_view(),name='update-course'),
    path('courses/<slug:slug>/delete/',CourseDeleteView.as_view(),name='delete-course'),

    # Sections
    path('courses/<slug:slug>/sections/create/',SectionCreateView.as_view(),name='create-section'),
    path('courses/<slug:slug>/sections/<int:section_id>/update/',SectionUpdateView.as_view(),name='update-section'),
    path('courses/<slug:slug>/sections/<int:section_id>/delete/',SectionDeleteView.as_view(),name='delete-section'),

    # Lessons
    path('courses/lessons/<int:lesson_id>/',LessonDetailView.as_view(),name='details-lesson'),
    path('courses/lessons/<int:lesson_id>/update/',LessonUpdateView.as_view(),name='update-lesson'),
    path('courses/lessons/<int:lesson_id>/delete/',LessonDeleteView.as_view(),name='delete-lesson'),
    path('courses/<slug:slug>/sections/<int:section_id>/lessons/create/',LessonCreateView.as_view(),name='create-lesson'),

]
router = DefaultRouter()
router.register('track-courses', TrackCourseViewSet,basename='track-courses')
urlpatterns += router.urls