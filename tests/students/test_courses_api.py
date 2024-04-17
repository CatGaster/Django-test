import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Course, Student
from tests.conftest import client ,student_factory, course_factory 


@pytest.mark.django_db
def test_get_cource(client, course_factory):
    #Arrange
    courses = course_factory()
    print(courses.id, courses.name)

    # Act
    response = client.get(f'/api/v1/courses/{courses.id}/')
    print(response)

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert courses.name == data['name']


@pytest.mark.django_db
def test_course_filter(client, course_factory):
    #Arrange
    courses_list = course_factory(_quantity=7)
    сourse = 5

    # Act
    response = client.get('/api/v1/courses/', {'id': courses_list[сourse].id, 'name': courses_list[сourse].name},)
    print(response.json())

    # Assert
    assert response.status_code == 200
    assert courses_list[сourse].id == response.json()[0]['id']
    assert courses_list[сourse].name == response.json()[0]['name']


@pytest.mark.django_db
def test_cources_list(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=20)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, course in enumerate(data):
        assert course['id'] == courses[i].id
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_create_cources(client,):
    #Arrange
    count = Course.objects.count()
    name = 'just tets words'
    
    # Act
    response_post = client.post('/api/v1/courses/', data = {'name': name})
    response_name = client.get(f'/api/v1/courses/?name={name}')
    response_json = client.get(f'/api/v1/courses/{response_post.json()["id"]}/')
    
    # Assert
    assert response_post.status_code == 201
    assert response_name.status_code == 200
    assert Course.objects.count() == count + 1
    assert name == response_json.json()['name']


@pytest.mark.django_db
def test_update_delete_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)

    # Act
    response_patch = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'Stil just tets words'})
    response_delete = client.delete(f'/api/v1/courses/{courses[1].id}/')
    response_get = client.get(f'/api/v1/courses/{courses[1].id}/')
    
    # Assert
    assert response_patch.status_code == 200
    assert response_delete.status_code == 204
    assert response_get.status_code == 404