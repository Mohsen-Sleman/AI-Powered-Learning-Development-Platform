from django.shortcuts import render
from .models import Track,Course,Section,CourseContent
from .serializers import CourseSerializer,SectionSerializer,CourseContentSerializer
from rest_framework.generics import RetrieveAPIView
# Create your views here.


class RetriveCourse(RetrieveAPIView) :
    lookup_field = 'slug'
    queryset = Course.objects.select_related('instructor').prefetch_related('sections__lessons').all()
    serializer_class = CourseSerializer

    