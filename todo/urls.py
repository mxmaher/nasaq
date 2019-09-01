from django.urls import path
from rest_framework.routers import DefaultRouter

from todo.views import StateFullTasksResource


router = DefaultRouter()
router.register(r'', StateFullTasksResource)

urlpatterns = router.urls