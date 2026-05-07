from rest_framework.generics import RetrieveAPIView,CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from users.permissions import IsInstructor
from courses.models import Track,Status
from courses.filters import TrackFilter
from users.models import RoleChoices
from courses.serializers import TrackListSerializer,TrackDetailSerializer,TrackWriteSerializer


class TrackListView(ListAPIView) :
    queryset = Track.objects.filter(status = Status.PUBLISHED).select_related('instructor')
    serializer_class = TrackListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = [{'difficulty_level': ['in', 'exact']},]
    filterset_class = TrackFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class TrackDetailView(RetrieveAPIView) :
    lookup_url_kwarg = 'track_id'
    serializer_class = TrackDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        base_queryset = Track.objects.prefetch_related('courses__enrollments')
        if user and user.is_authenticated and user.role == RoleChoices.INSTRUCTOR :
            return base_queryset.filter(Q(instructor = user) | Q(status = Status.PUBLISHED))
        return base_queryset.filter(status = Status.PUBLISHED)

class TrackCreateView(CreateAPIView) :
    serializer_class = TrackWriteSerializer
    permission_classes = [IsAuthenticated,IsInstructor]
    
    def perform_create(self, serializer):
        serializer.save(instructor = self.request.user)
    

class TrackUpdateView(UpdateAPIView) :
    lookup_url_kwarg = 'track_id'
    serializer_class = TrackWriteSerializer
    permission_classes = [IsAuthenticated,IsInstructor]

    def get_queryset(self):
        return Track.objects.filter(instructor = self.request.user)
    

class TrackDeleteView(DestroyAPIView) :
    lookup_url_kwarg = 'track_id'
    permission_classes = [IsAuthenticated,IsInstructor]

    def get_queryset(self):
        return Track.objects.filter(instructor = self.request.user)
    



