from django.urls import path
from .views import (
    TaskListAPIView,
    TaskCreateAPIView,
    TaskRetrieveAPIView,
    TaskUpdateAPIView,
    TaskDeleteAPIView,
)

urlpatterns = [
    path("task-list/", TaskListAPIView.as_view()),             # GET (list)
    path("create/", TaskCreateAPIView.as_view()),     # POST
    path("task/<int:pk>/", TaskRetrieveAPIView.as_view()), # GET (detail)
    path("update-task/<int:pk>/", TaskUpdateAPIView.as_view()),  # PUT/PATCH
    path("delete-task/<int:pk>/", TaskDeleteAPIView.as_view()),  # DELETE
]
