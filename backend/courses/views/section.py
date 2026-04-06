from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsInstructor
from courses.models import Course,Section
from courses.serializers import SectionWriteSerializer

class SectionCreateView(CreateAPIView) :
    serializer_class = SectionWriteSerializer
    permission_classes = [IsAuthenticated,IsInstructor]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        course_slug = self.kwargs.get("slug")
        course = get_object_or_404(Course,slug = course_slug,instructor = self.request.user)
        serializer.save(course = course)

class SectionUpdateView(UpdateAPIView) :
    lookup_url_kwarg = 'section_id'
    serializer_class = SectionWriteSerializer
    permission_classes = [IsAuthenticated,IsInstructor]

    def update(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        course = get_object_or_404(Course,slug =slug,instructor = request.user)
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return Section.objects.filter(course__instructor = self.request.user)

class SectionDeleteView(DestroyAPIView) :
    lookup_url_kwarg = 'section_id'
    permission_classes = [IsAuthenticated,IsInstructor]

    def get_object(self):
        course_slug = self.kwargs.get('slug')
        section_id = self.kwargs.get('section_id')
        course = get_object_or_404(Course,slug = course_slug,instructor = self.request.user)
        section = get_object_or_404(Section,course = course,id = section_id)
        return section
    
    def get_queryset(self):
        return Section.objects.filter(course__instructor = self.request.user)
