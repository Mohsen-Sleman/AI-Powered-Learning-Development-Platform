
from rest_framework import serializers
from users.models import User
from .models import Track,Course,Section,CourseContent


class CourseContentSerializer(serializers.ModelSerializer) :

    class Meta :
        model = CourseContent
        fields = [
            'id',
            'title',
            'content_type',
            'video_url',
            'file',
            'external_link',
            'order',
            'created_at',
        ]

class SectionSerializer(serializers.ModelSerializer) :
    lessons = CourseContentSerializer(many=True,read_only=True)
    class Meta :
        model = Section
        fields = [
            'id',
            'title',
            'description',
            'order',
            'created_at',
            'lessons',
        ]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = [
            'id',
            'full_name'
        ]

class CourseSerializer(serializers.ModelSerializer) :
    instructor = AuthorSerializer(read_only = True)
    sections = SectionSerializer(many=True,read_only=True)
    class Meta :
        model = Course
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'difficulty_level',
            'thumbnail',
            'instructor',
            'status',
            'created_at',
            'sections',
        ]