from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from courses.models import Track,Course,Enrollment,TrackEnrollment
from courses.serializers import EnrollmentSerializer,EnrollmenTracktSerializer
from courses.filters import EnrollmentCourseFilter,EnrollmentTrackFilter


class UserEnrollmentCreateView(CreateAPIView,DestroyAPIView) :
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user = self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data , context = {'request' : request})
        serializer.is_valid(raise_exception = True)

        course = serializer.validated_data.get('course')
        if Enrollment.objects.filter(course = course,user = request.user).exists() :
            raise ValidationError({'detail' :'You are already enrolled in this course.'})
        
        if Course.objects.filter(instructor = request.user).exists() :
            raise ValidationError({'detail' : 'Instructor Cannot enroll in their own course'})

        self.perform_create(serializer)

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):

        serializer.save(user = self.request.user)


class ListUserEnrollmentView(ListAPIView) :
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = EnrollmentCourseFilter
    ordering_fields = ['enrolled_at']
    ordering = ['-enrolled_at']

    def get_queryset(self):
        user = self.request.user
        difficulty = self.request.query_params.get('difficulty_level')
        instructor = self.request.query_params.get('instructor')
        queryset = Enrollment.objects.filter(user = user).select_related('course__instructor')
        if difficulty :
            queryset = queryset.filter(course__difficulty_level = difficulty)
        if instructor :
            queryset = queryset.filter(course__instructor = instructor)
        return queryset

class ProgressEnrollmentUpdateView(APIView) :

    def patch(self,request,slug) :
        course = get_object_or_404(Course,slug = slug)
        enrollment = get_object_or_404(Enrollment,user=request.user,course = course)
        lesson_order = request.data.get('lesson_order')

        if lesson_order is None :
            return Response({'error' : 'lesson_order is required'},status=status.HTTP_400_BAD_REQUEST)
        if not str(lesson_order).isdigit() :
            return Response({'error' : 'Must Be Integer'},status=status.HTTP_400_BAD_REQUEST)
        enrollment.progress = lesson_order
        enrollment.save()
        return Response({'message' : 'Progress updated successfully' , 'progress' : enrollment.progress},status=status.HTTP_200_OK)

class UserEnrollmentTrackCreateView(CreateAPIView,DestroyAPIView) :
    queryset = TrackEnrollment
    serializer_class = EnrollmenTracktSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TrackEnrollment.objects.filter(user = self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data , context = {'request' : request})
        serializer.is_valid(raise_exception = True)

        track = serializer.validated_data.get('track')
        if TrackEnrollment.objects.filter(track = track,user = request.user).exists() :
            raise ValidationError({'detail' :'You are already enrolled in this track.'})
        
        if Track.objects.filter(instructor = request.user).exists() :
            raise ValidationError({'detail' : 'Instructor Cannot enroll in their own track'})

        self.perform_create(serializer)

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def perform_create(self, serializer):

        serializer.save(user = self.request.user)
        
class ListUserTrackEnrollmentView(ListAPIView) :

    serializer_class = EnrollmenTracktSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_class = EnrollmentTrackFilter
    ordering_fields = ['enrolled_at']
    ordering = ['-enrolled_at']

    def get_queryset(self):
        user = self.request.user
        difficulty = self.request.query_params.get('difficulty_level')
        instructor = self.request.query_params.get('instructor')
        queryset = TrackEnrollment.objects.filter(user = user).select_related('track__instructor').prefetch_related('track')
        if difficulty :
            queryset = queryset.filter(track__difficulty_level = difficulty)
        if instructor :
            queryset = queryset.filter(track__instructor = instructor)
        return queryset