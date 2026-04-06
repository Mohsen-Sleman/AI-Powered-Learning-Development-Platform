from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser,FormParser
from users.serializers import RegisterSerializer

# Create your views here.

class RegisterView(CreateAPIView) :
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser,FormParser]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data,context={'request' : request})
        
        serializer.is_valid(raise_exception = True)
        user = serializer.save()
        profile = None
        if user.profile_picture :
            profile = user.profile_picture.url
        return Response({
            "id" : user.id,
            "email" : user.email,
            "full_name" : user.full_name,
            "role" : user.role,
            "profile_picture" : profile
        },status = status.HTTP_201_CREATED)
