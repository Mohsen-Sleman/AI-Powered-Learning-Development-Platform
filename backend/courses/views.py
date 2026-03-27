from django.shortcuts import render
from .models import Track,Course,Section,CourseContent,Enrollment
from .serializers import CourseSerializer,SectionSerializer,CourseContentSerializer,EnrollmentSerializer,CourseListSerializer,EnrollmentCourseSerializer
from rest_framework.generics import RetrieveAPIView,CreateAPIView,ListAPIView,UpdateAPIView,GenericAPIView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.


class RetriveCourse(RetrieveAPIView) :
    lookup_field = 'slug'
    queryset = Course.objects.select_related('instructor').prefetch_related('sections__lessons').all()
    serializer_class = CourseSerializer


class CreateUserEnrollment(CreateAPIView) :
    serializer_class = EnrollmentSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class ListUserEnrollment(ListAPIView) :
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(user = self.request.user).select_related('course__instructor')
    
class ProgressEnrollmentUpdateApiView(APIView) :

    def patch(self,request,slug) :
        course = get_object_or_404(Course,slug = slug)
        enrollment = get_object_or_404(Enrollment,user=request.user,course = course)
        lesson_order = request.data.get('lesson_order')

        if lesson_order is None :
            return Response({'error' : 'lesson_order is required'},status=status.HTTP_400_BAD_REQUEST)
        
        enrollment.progress = lesson_order
        enrollment.save()
        return Response({'message' : 'Progress updated successfully' , 'progress' : enrollment.progress})
        

class CourseListView(ListAPIView) :
    queryset = Course.objects.filter(status = Course.Status.PUBLISHED).select_related('instructor').only('name','slug','thumbnail','difficulty_level','instructor__id','instructor__full_name')
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['instructor','difficulty_level']
    search_fields = ['name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']