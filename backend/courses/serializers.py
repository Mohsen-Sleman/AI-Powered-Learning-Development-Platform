
from rest_framework import serializers
from users.models import User
from .models import Track,Course,Section,CourseContent,Enrollment


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

class EnrollmentSerializer(serializers.ModelSerializer) :
    percentage = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    class Meta :
        model = Enrollment
        fields = [
            'course',
            'progress',
            'percentage',
            'completed',
            'enrolled_at'
        ]
        read_only_fields = ['progress','enrolled_at']
    def to_representation(self, instance):
        instance._total_lessons = CourseContent.objects.filter(
            section__course=instance.course
        ).count()
        return super().to_representation(instance)
    

    def get_percentage(self,obj) :
        total_lessons = getattr(obj,'_total_lessons',0)
        if total_lessons == 0 :
            return 0
        progress = min(obj.progress,total_lessons)
        return round(progress/total_lessons * 100,2)
    
    def get_completed(self,obj) :
        total_lessons = getattr(obj,'_total_lessons',0)
        if total_lessons == 0:
            return False
        return obj.progress >= total_lessons



class CourseListSerializer(serializers.ModelSerializer) :
    instructor = AuthorSerializer(read_only = True)
    class Meta : 
        model = Course
        fields = [
            'name',
            'slug',
            'thumbnail',
            'instructor',
            'difficulty_level',
        ]