import pytest
from django.urls import reverse
from rest_framework import status
from courses.models import Enrollment

@pytest.mark.django_db
def test_enroll_user_in_course_success(client,instructor_user,student_user,create_course,image) :
    course = create_course("First Course",instructor_user,image)
    client.force_authenticate(user = student_user)
    url = reverse('create-user-course-enroll')
    response = client.post(url,data={'course' : course.pk})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['course_details']['id'] == course.pk
    assert Enrollment.objects.filter(course = course,user = student_user).exists()
    assert Enrollment.objects.count() == 1

@pytest.mark.django_db
def test_enroll_user_in_same_course_twice(client,instructor_user,student_user,create_course,image) :
    course = create_course("First Course",instructor_user,image)
    client.force_authenticate(user = student_user)
    url = reverse('create-user-course-enroll')
    first_response = client.post(url,data={'course' : course.pk})

    assert first_response.status_code == status.HTTP_201_CREATED
    
    response = client.post(url,data={'course' : course.pk})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert str(response.data['detail']).lower() == 'you are already enrolled in this course.'
    assert Enrollment.objects.filter(course=course,user=student_user).count() == 1

@pytest.mark.django_db
def test_unauthorized_user_cannot_enroll_in_course(client,instructor_user,create_course,image) :
    course = create_course("First Course",instructor_user,image)
    url = reverse('create-user-course-enroll')
    response = client.post(url,data={'course' : course.pk})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert str(response.data['detail']).lower() == 'authentication credentials were not provided.'
    assert not Enrollment.objects.filter(course = course).exists()

@pytest.mark.django_db
def test_enroll_user_in_nonexistent_course(client,student_user) :

    client.force_authenticate(user = student_user)
    url = reverse('create-user-course-enroll')
    response = client.post(url,data={'course' : 999})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['course'][0].code == 'does_not_exist'
    assert not Enrollment.objects.filter(user = student_user).exists()
    assert Enrollment.objects.count() == 0