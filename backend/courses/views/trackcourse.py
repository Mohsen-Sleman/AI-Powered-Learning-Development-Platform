from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from users.permissions import IsInstructor
from courses.models import Track,Course,TrackCourse
from courses.serializers import TrackCourseSerializer


class TrackCourseViewSet(GenericViewSet,CreateModelMixin,DestroyModelMixin) :
    queryset = TrackCourse.objects.all()
    permission_classes = [IsAuthenticated,IsInstructor]
    serializer_class = TrackCourseSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        track_id = self.request.data.get('track')
        course_id = self.request.data.get('course')
        
        track = get_object_or_404(Track,id = track_id,instructor = user)
        course = get_object_or_404(Course,id = course_id,instructor = user)
        
        order = TrackCourse.objects.filter(track = track).count() + 1
        serializer.save(track = track,course = course,order = order)

    def perform_destroy(self, instance):
        user = self.request.user
        track = instance.track
        course = instance.course
        
        if track.instructor != user or course.instructor != user :
            raise PermissionDenied
        instance.delete()
        tcs = TrackCourse.objects.filter(track = track).order_by('order')
        order = 1
        for track_course in tcs: 
            track_course.order = order
            track_course.save()
            order += 1

    @action(detail=False,methods=["PATCH"],url_path='reorder-courses')
    def reorder(self,request) :
        user = request.user
        track_id = request.data.get('track_id')
        print(track_id)
        track = get_object_or_404(Track,id = track_id,instructor = user)
        courses_data = request.data.get('courses_data')

        if not courses_data :
            raise ValidationError('No courses data provided')
        
        course_ids = [item['course_id'] for item in courses_data]
        track_courses_qs = TrackCourse.objects.filter(track=track,course_id__in = course_ids)

        if track_courses_qs.count() != len(course_ids) :
            raise ValidationError('One or more courses do not belong to this track')
        
        orders = [item['order'] for item in courses_data]
        expected_order = list(range(1,len(orders)+1))

        if sorted(orders) != expected_order :
            raise ValidationError('Invalid sequence: Order numbers must be consecutive and start from 1')
        
        for item in courses_data :
            tc = TrackCourse.objects.get(track = track,course_id = item['course_id'])
            tc.order = item['order']
            tc.save()

        return Response({
            "status" : "success",
            "message" : "Course reordered successfully",
            "track_id" : track.id,
            "total_courses" : len(courses_data)
        },status=status.HTTP_200_OK)