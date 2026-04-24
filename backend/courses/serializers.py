
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from users.models import User
from courses.models import Track,Course,Section,CourseContent,Enrollment,TrackCourse,TrackEnrollment
from courses.models import Status


class AuthorSerializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = [
            'id',
            'full_name'
        ]

class LessonSerializer(serializers.ModelSerializer) :

    class Meta :
        model = CourseContent
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'content_type',
            'video_url',
            'file',
            'external_link',
            'order',
            'created_at',
        ]

class CourseMiniSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Course
        fields = [
            'id',
            'name',
            'slug',
        ]
class SectionMiniSerializer(serializers.ModelSerializer) :
    course = CourseMiniSerializer(read_only = True)
    class Meta : 
        model = Section
        fields = [
            'id',
            'title',
            'course',
        ]

class LessonDetailSerializers(serializers.ModelSerializer) :
    section = SectionMiniSerializer(read_only = True)
    class Meta : 
        model = CourseContent
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'content_type',
            'video_url',
            'file',
            'external_link',
            'order',
            'section',
        ]

class LessonWriteSerializer(serializers.ModelSerializer) :

    class Meta :
        model = CourseContent
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'content_type',
            'video_url',
            'file',
            'external_link',
            'order',
            'section',
        ]
        read_only_fields = ['section']

class SectionSerializer(serializers.ModelSerializer) :
    lessons = LessonSerializer(many=True,read_only=True)
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

class SectionWriteSerializer(serializers.ModelSerializer) :

    class Meta :
        model = Section
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course',
        ]
        read_only_fields = ['course']

    def validate(self, attrs):
        course_slug = self.context['view'].kwargs.get('slug')
        course = get_object_or_404(Course,slug = course_slug)
        order = attrs.get('order')
        
        if Section.objects.filter(course=course, order=order).exists():
            raise serializers.ValidationError({"order": "This order already exists in this course."})
        return attrs


class CourseDetailSerializer(serializers.ModelSerializer) :
    instructor = AuthorSerializer(read_only = True)
    sections = SectionSerializer(many=True,read_only=True)
    completed = serializers.SerializerMethodField(read_only = True)
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
            'completed',
            'sections',
        ]
        
    def get_completed(self,obj) :
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        enrollment = obj.enrollments.filter(user = request.user).first()
        if enrollment:
            return EnrollmentSerializer(enrollment).data.get('completed')
        return False

class CourseListSerializer(serializers.ModelSerializer) :
    instructor = AuthorSerializer(read_only = True)
    completed = serializers.SerializerMethodField(read_only = True)
    class Meta : 
        model = Course
        fields = [
            'id',
            'name',
            'slug',
            'thumbnail',
            'instructor',
            'difficulty_level',
            'created_at',
            'completed',
        ]
    def get_completed(self,obj) :
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        enrollment = obj.enrollments.filter(user = request.user).first()
        if enrollment:
            return EnrollmentSerializer(enrollment).data.get('completed')
        return False

class CourseWriteSerializer(serializers.ModelSerializer) :

    class Meta : 
        model = Course
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'thumbnail',
            'difficulty_level',
            'status',
        ]
        read_only_fields = ['slug']

class EnrollmentCourseSerializer(serializers.ModelSerializer) :
    instructor = AuthorSerializer(read_only = True)
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
            'created_at',
        ]

class EnrollmentSerializer(serializers.ModelSerializer) :
    course = serializers.PrimaryKeyRelatedField(
        queryset = Course.objects.all(),
        write_only = True
    )
    course_details = EnrollmentCourseSerializer(source='course',read_only = True)
    percentage = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    class Meta :
        model = Enrollment
        fields = [
            'id',
            'course',
            'course_details',
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
        return round((progress/total_lessons) * 100,2)
    
    def get_completed(self,obj) :
        total_lessons = getattr(obj,'_total_lessons',0)
        if total_lessons == 0:
            return False
        return obj.progress >= total_lessons
    

class CourseWithProgressSerializer(serializers.ModelSerializer) :
    completed = serializers.SerializerMethodField()
    class Meta : 
        model = Course
        fields = [
            'id',
            'name',
            'slug',
            'thumbnail',
            'difficulty_level',
            'created_at',
            'completed',
        ]
    def get_completed(self,obj) :
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        enrollment = obj.enrollments.filter(user = request.user).first()
        if enrollment:
            return EnrollmentSerializer(enrollment).data.get('completed')
        return False


class TrackListSerializer(serializers.ModelSerializer) :
    instructor = AuthorSerializer(read_only=True)
    courses_count = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    class Meta :
        model = Track
        fields = [
            'id',
            'name',
            'description',
            'thumbnail',
            'difficulty_level',
            'instructor',
            'created_at',
            'courses_count',
            'percentage',
            'completed',
        ]

    def _get_user_progress(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 0, 0

        published_courses = obj.courses.filter(status=Status.PUBLISHED)
        total_count = published_courses.count()
        if total_count == 0:
            return 0, 0

        completed_count = 0
        for course in published_courses:
            enrollment = course.enrollments.filter(user=request.user).first()
            if enrollment:
                is_done = EnrollmentSerializer(enrollment, context=self.context).data.get('completed', False)
                if is_done:
                    completed_count += 1
        
        return completed_count, total_count

    def get_courses_count(self, obj):
        return obj.courses.filter(status=Status.PUBLISHED).count()

    def get_percentage(self, obj):
        completed, total = self._get_user_progress(obj)
        if total == 0: return 0.00
        return round((completed / total) * 100, 2)

    def get_completed(self, obj):
        completed, total = self._get_user_progress(obj)
        return total > 0 and completed >= total

class TrackCourseDetailSerializer(serializers.ModelSerializer) :
    course = CourseWithProgressSerializer(read_only=True)
    track_course_id = serializers.IntegerField(source = 'id',read_only = True)
    class Meta : 
        model = TrackCourse
        fields = [
            'track_course_id',
            'course',
            'order',
        ]

class TrackDetailSerializer(serializers.ModelSerializer) :
    courses = TrackCourseDetailSerializer(source = 'track_courses',many = True,read_only = True)
    class Meta :
        model = Track
        fields = [
            'id',
            'name',
            'description',
            'thumbnail',
            'difficulty_level',
            'created_at',
            'courses',
        ]


class TrackWriteSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Track
        fields = [
            'id',
            'name',
            'description',
            'thumbnail',
            'difficulty_level',
        ]


class EnrollmenTracktSerializer(serializers.ModelSerializer) :
    track = serializers.PrimaryKeyRelatedField(
        queryset = Track.objects.all(),
        write_only = True
    )
    track_detail = TrackListSerializer(source = 'track',read_only = True)
    class Meta :
        model = TrackEnrollment
        fields = [
            'id',
            'track',
            'track_detail',
            'score',
            'is_completed',
            'enrolled_at',
        ]
        read_only_fields = ['score','is_completed','enrolled_at']


class TrackCourseSerializer(serializers.ModelSerializer) :

    class Meta : 
        model = TrackCourse
        fields = [
            'id',
            'track',
            'course',
            'order',
        ]
        read_only_fields = ['order']