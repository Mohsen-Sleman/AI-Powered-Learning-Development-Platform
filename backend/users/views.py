from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser,FormParser
from users.serializers import RegisterSerializer,ProfileSerializer,MyTokenObtainPairSerializer

# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView) :
    serializer_class = MyTokenObtainPairSerializer


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


class ProfileView(RetrieveUpdateAPIView) :
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

class LogoutView(APIView) :
    permission_classes = [AllowAny]

    def post(self,request) :
        try :
            refresh_token = request.data.get('refresh')
            if not refresh_token :
                return Response({"detail" : "Refresh token is required"},status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        