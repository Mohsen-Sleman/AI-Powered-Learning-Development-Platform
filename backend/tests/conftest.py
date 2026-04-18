from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from courses.models import Course,Level,Status
from users.models import User,RoleChoices

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def image(): 
    
    with open("tests/assets/test.jpg","rb") as img :
        return SimpleUploadedFile(
            name="test.jpg",
            content=img.read(),
            content_type="image/jpeg"
        )

@pytest.fixture
def instructor_user(image):
    user = User.objects.create_user(full_name="test",
                        email="pytest2@gmail.com",
                        profile_picture = image,
                        role = RoleChoices.INSTRUCTOR,
                        password="Testpass123!")
    return user

@pytest.fixture
def student_user(image):
    user = User.objects.create_user(full_name="test",
                        email="pytest3@gmail.com",
                        profile_picture = image,
                        role = RoleChoices.STUDENT,
                        password="Testpass123!")
    return user

@pytest.fixture
def create_course() :
    def _create_course(name,instructor,image,difficulty_level=Level.BEGINNER) :
        return Course.objects.create(name=name,
                                description='desc',
                                instructor = instructor,
                                difficulty_level = difficulty_level,
                                thumbnail = image,
                                status = Status.PUBLISHED)
    return _create_course

@pytest.fixture
def client():
    return APIClient()

