from http import HTTPMethod

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status as st

from tasks.models import Task

from .factory import client, task, tasks


@pytest.mark.django_db
def test_task_list_all(client, tasks):
    assert Task.objects.all().count() == 5

    response = client.get(
        path=reverse("tasks:task-list"),
    )
    assert response.status_code == st.HTTP_200_OK
    assert len(response.data) == 5
    assert response.data[0].get("title") == tasks[0].title


@pytest.mark.django_db
def test_test_get_item(client, task):
    assert Task.objects.all().count() == 1
    assert task.id == Task.objects.first().pk

    response = client.get(
        path=reverse("tasks:task-detail", args=[task.id]),
    )
    assert response.status_code == st.HTTP_200_OK
    assert response.data.get("title") == task.title


@pytest.mark.django_db
def test_create_item(client):
    task = dict(
        title=Faker().sentence(),
        description=Faker().paragraph(),
        done=False,
    )

    response = client.post(
        path=reverse("tasks:task-list"),
        data=task,
    )

    assert Task.objects.all().count() == 1
    assert response.status_code == st.HTTP_201_CREATED
    assert response.data.get("title") == task.get("title")


@pytest.mark.django_db
def test_create_item__required_fields(client):
    task = dict(
        title=Faker().sentence(),
        description=Faker().paragraph(),
        done=Faker().boolean(),
    )

    required_fields = ("title", "description")

    for field in required_fields:
        subject = {**task}
        del subject[field]

        response = client.post(
            path=reverse("tasks:task-list"),
            data=subject,
        )

        assert Task.objects.all().count() == 0, f"> Field: {field}"
        assert response.status_code == st.HTTP_400_BAD_REQUEST, f"> Field: {field}"
        assert response.data.get(field)[0].code == "required", f"> Field: {field}"


@pytest.mark.django_db
def test_create_item__done_is_false_by_default(client):
    task = dict(
        title=Faker().sentence(),
        description=Faker().paragraph(),
    )

    response = client.post(
        path=reverse("tasks:task-list"),
        data=task,
    )

    assert Task.objects.all().count() == 1
    assert response.status_code == st.HTTP_201_CREATED
    assert response.data.get("done") == False


@pytest.mark.django_db
def test_update_item_field(client, task):
    subject = dict(
        title=Faker().sentence(),
        description=Faker().paragraph(),
        done=True,
    )

    fields_to_update = ["title", "description", "done"]
    for field in fields_to_update:
        response = client.patch(
            path=reverse("tasks:task-detail", args=[task.id]),
            data={field: subject.get(field)},
        )

        assert response.status_code == st.HTTP_200_OK, f"Field: {field}"
        assert response.data.get(field) == subject.get(field), f"Field: {field}"
        task_db = Task.objects.get(pk=task.id)
        assert getattr(task_db, field) == subject.get(field)


@pytest.mark.django_db
def test_update_item(client, task):
    task_db = Task.objects.first()

    subject = dict(
        title=Faker().sentence(),
        description=Faker().paragraph(),
        done=Faker().boolean(),
    )

    response = client.put(
        path=reverse("tasks:task-detail", args=[task.id]),
        data=subject,
    )

    assert response.status_code == st.HTTP_200_OK
    assert response.data.get("title") == subject.get("title")
    assert response.data.get("description") == subject.get("description")
    assert response.data.get("done") == subject.get("done")
    assert response.data.get("title") != task_db.title
    assert response.data.get("description") != task_db.description


@pytest.mark.django_db
def test_delete_item(client, task):
    assert Task.objects.all().count() == 1

    response = client.delete(
        path=reverse("tasks:task-detail", args=[task.id]),
    )

    assert Task.objects.all().count() == 0
    assert response.status_code == st.HTTP_204_NO_CONTENT
    assert response.data.get("message") == task.title


@pytest.mark.django_db
def test_mark_as_done(client):
    task = Task.objects.create(
        title=Faker().sentence(), description=Faker().paragraph(), done=False
    )

    response = client.patch(path=reverse("tasks:task-mark-done", args=[task.pk]))

    assert response.status_code == st.HTTP_200_OK
    assert response.data.get("title") == task.title
    assert response.data.get("done") == True


@pytest.mark.django_db
def test_404_if_task_not_exist(client):
    allowed_methods = [
        HTTPMethod.GET,
        HTTPMethod.PUT,
        HTTPMethod.PATCH,
        HTTPMethod.DELETE,
    ]

    for method in allowed_methods:
        response = getattr(client, method.lower())(
            path=reverse("tasks:task-detail", args=[0])
        )

        assert response.status_code == st.HTTP_404_NOT_FOUND
