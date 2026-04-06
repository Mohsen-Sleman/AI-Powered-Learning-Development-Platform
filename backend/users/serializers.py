from rest_framework import serializers
from users.models import User,RoleChoices

class RegisterSerializer(serializers.ModelSerializer) :
    password2 = serializers.CharField(write_only = True)
    role = serializers.CharField(required = False,default = RoleChoices.STUDENT)
    profile_picture = serializers.ImageField(required = False,allow_null = True)
    class Meta : 
        model = User
        fields = [
            'email',
            'full_name',
            'password',
            'password2',
            'role',
            'profile_picture'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.profile_picture and request :
            data['profile_picture'] = request.build_absolute_uri(instance.profile_picture.url)
        else :
            data['profile_picture'] = None
        return data

    def validate(self, attrs):
        if attrs['password'] != attrs['password2'] :
            raise serializers.ValidationError('Passwords do not match')
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(email=validated_data['email'],
                                        full_name=validated_data['full_name'],
                                        password=validated_data['password'],
                                        role=validated_data['role'],
                                        profile_picture=validated_data['profile_picture'])