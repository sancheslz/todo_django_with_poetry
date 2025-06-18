from factory import django, faker
from pytest import fixture
from rest_framework.test import APIClient

from tasks.models import Task


class TaskFaker(django.DjangoModelFactory):
    class Meta:
        model = Task

    title = faker.Faker("sentence")
    description = faker.Faker("paragraph")
    done = faker.Faker("boolean")


@fixture
def client():
    return APIClient()


@fixture
def task():
    return TaskFaker.create()


@fixture
def tasks(elements=5):
    return TaskFaker.create_batch(elements)
