from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from users.permissions import IsInstructor
from courses.models import Course,Section,CourseContent,Status
from users.models import RoleChoices
from courses.serializers import LessonWriteSerializer,LessonDetailSerializers


class LessonDetailView(RetrieveAPIView) :
    lookup_url_kwarg = 'lesson_id'
    serializer_class = LessonDetailSerializers

    def get_queryset(self):
        user = self.request.user
        base_queryset = CourseContent.objects.select_related('section__course')
        if user and user.is_authenticated and user.role == RoleChoices.INSTRUCTOR :
            return base_queryset.filter(Q(section__course__instructor = user) | Q(section__course__status = Status.PUBLISHED))
        return base_queryset.filter(section__course__status = Status.PUBLISHED)

class LessonCreateView(CreateAPIView) :
    serializer_class = LessonWriteSerializer
    permission_classes = [IsAuthenticated,IsInstructor]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        course_slug = self.kwargs.get('slug')
        course = get_object_or_404(Course,slug = course_slug)
        section_id = self.kwargs.get('section_id')
        section = get_object_or_404(Section,id = section_id,course = course)
        order = serializer.validated_data.get('order')

        if CourseContent.objects.filter(section=section, order=order).exists():
            raise ValidationError({"order": "This order already exists in this course."})
        
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        course_slug = self.kwargs.get("slug")
        section_id = self.kwargs.get('section_id')
        course = get_object_or_404(Course,slug = course_slug)
        section = get_object_or_404(Section,id = section_id,course=course)
        serializer.save(section = section)

class LessonUpdateView(UpdateAPIView) :
    lookup_url_kwarg = 'lesson_id'
    serializer_class = LessonWriteSerializer
    permission_classes = [IsAuthenticated,IsInstructor]

    def get_queryset(self):
        return CourseContent.objects.filter(section__course__instructor = self.request.user)


class LessonDeleteView(DestroyAPIView) :
    lookup_url_kwarg = 'lesson_id'
    permission_classes = [IsAuthenticated,IsInstructor]

    def get_queryset(self):
        return CourseContent.objects.filter(section__course__instructor = self.request.user)
