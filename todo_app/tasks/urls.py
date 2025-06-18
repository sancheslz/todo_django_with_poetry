from django.urls import path
from rest_framework.routers import SimpleRouter

from tasks.views.api import task

app_name = "tasks"
router = SimpleRouter()
router.register(r"task", task.TaskViewSet, basename="task")

urlpatterns = [] + router.urls
