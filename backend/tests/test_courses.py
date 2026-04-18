from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
import pytest 
from courses.models import Level
from users.models import User,RoleChoices

User = get_user_model()


@pytest.mark.django_db
def test_get_all_courses_return_published_courses(client,instructor_user,image,create_course) :
    create_course('First Course',instructor_user,image)
    create_course('Second Course',instructor_user,image)
    url = reverse('list-courses')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert len(response.data['results']) == 2

    names = [course['name'] for course in response.data['results']]

    assert "First Course" in names
    assert "Second Course" in names

@pytest.mark.django_db
def test_get_courses_empty(client) :
    url = reverse('list-courses')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 0

@pytest.mark.django_db
def test_get_courses_filter_by_difficulty(client,instructor_user,image,create_course) :
    create_course('First Course',instructor_user,image,difficulty_level=Level.BEGINNER)
    create_course('Second Course',instructor_user,image,difficulty_level=Level.BEGINNER)
    create_course('Third Course',instructor_user,image,difficulty_level=Level.ADVANCED)

    url = reverse('list-courses')
    response = client.get(url,data = {"difficulty_level" : Level.BEGINNER})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2

    difficulty_levels = [course['difficulty_level'] for course in response.data['results']]

    assert all(level == Level.BEGINNER for level in difficulty_levels)

@pytest.mark.django_db
def test_get_courses_filter_by_name(client,instructor_user,image,create_course) :
    create_course('First Course',instructor_user,image)
    create_course('First Course -2-',instructor_user,image)
    create_course('Third Course',instructor_user,image)

    url = reverse('list-courses')
    response = client.get(url,data = {'search' : 'First'})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2

    names = [course['name'] for course in response.data['results']]

    assert all("First" in name for name in names)


@pytest.mark.django_db
def test_get_courses_filter_by_instructor(client,instructor_user,image,create_course) :
    instructor2 = User.objects.create_user(full_name="test2",
                        email='test2@gmail.com',
                        profile_picture = image,
                        role = RoleChoices.INSTRUCTOR,
                        password="Testpass123!")
    
    create_course('First Course',instructor_user,image)
    create_course('Second Course',instructor_user,image)
    create_course('Third Course',instructor2,image)

    url = reverse('list-courses')
    response = client.get(url,data = {'instructor' : instructor_user.pk})
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2

    instructors = [course['instructor'] for course in response.data['results']]

    assert all(instructor['id'] == instructor_user.pk for instructor in instructors)

@pytest.mark.django_db
def test_update_course_successfully(client,instructor_user,image,create_course) :
    course = create_course("First Course",instructor_user,image)
    url = reverse('update-course',kwargs={'slug' : course.slug})
    client.force_authenticate(user = instructor_user)
    response = client.patch(url,data = {'name' : 'First Course Updated'})

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'First Course Updated'

    course.refresh_from_db()
    assert course.name == "First Course Updated"

@pytest.mark.django_db
def test_update_course_with_unauthorized_user(client,instructor_user,image,create_course) :
    course = create_course("First Course",instructor_user,image)
    url = reverse('update-course',kwargs={'slug' : course.slug})
    response = client.patch(url,data = {'name' : 'First Course Updated'})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    course.refresh_from_db()
    assert course.name == 'First Course'

@pytest.mark.django_db
def test_student_cannot_update_course(client,instructor_user,student_user,image,create_course) :
    course = create_course("First Course",instructor_user,image)
    url = reverse('update-course',kwargs={'slug' : course.slug})
    client.force_authenticate(user = student_user)
    response = client.patch(url,data = {'name' : 'First Course Updated'})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert str(response.data['detail']).lower() == 'you do not have permission to perform this action.'

    course.refresh_from_db()
    assert course.name == 'First Course'

@pytest.mark.django_db
def test_instructor_cannot_update_other_instructor_course(client,instructor_user,image,create_course) :
    course = create_course("First Course",instructor_user,image)
    instructor2 = User.objects.create_user(full_name="test2",
                        email='test2@gmail.com',
                        profile_picture = image,
                        role = RoleChoices.INSTRUCTOR,
                        password="Testpass123!")
    
    url = reverse('update-course',kwargs={'slug' : course.slug})
    client.force_authenticate(user = instructor2)
    response = client.patch(url,data = {'name' : 'First Course Updated'})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert str(response.data['detail']).lower() == 'no course matches the given query.'
    
    course.refresh_from_db()
    assert course.name == 'First Course'