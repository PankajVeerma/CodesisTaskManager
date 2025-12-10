from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAdminOrOwner


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "description"]
    filterset_fields = ["status"]
    pagination_class = PageNumberPagination

    def get(self, request):
        try:
            user = request.user

            # RBAC: admin → all tasks, user → own tasks
            if user.groups.filter(name="Admin").exists():
                queryset = Task.objects.all()
            else:
                queryset = Task.objects.filter(owner=user)

            # Apply filters & search manually
            for backend in list(self.filter_backends):
                queryset = backend().filter_queryset(request, queryset, self)

            # Pagination
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)

            serializer = TaskSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Failed to fetch tasks", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TaskCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    def post(self, request):
        serializer = TaskSerializer(data=request.data)

        try:
            with transaction.atomic():
                if serializer.is_valid():
                    serializer.save(owner=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": "Task creation failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class TaskRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get(self, request, pk):
        try:
            task = Task.objects.filter(pk=pk).first()

            if not task:
                return Response({"error": "Task not found"}, status=404)

            self.check_object_permissions(request, task)
            serializer = TaskSerializer(task)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": "Failed to fetch task", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )



class TaskUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def put(self, request, pk):
        try:
            task = Task.objects.filter(pk=pk).first()
            if not task:
                return Response({"error": "Task not found"}, status=404)

            self.check_object_permissions(request, task)

            serializer = TaskSerializer(task, data=request.data, partial=False)

            with transaction.atomic():
                if serializer.is_valid():
                    serializer.save(owner=task.owner)  # owner should not change
                    return Response(serializer.data)

                return Response(serializer.errors, status=400)

        except Exception as e:
            return Response(
                {"error": "Failed to update task", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request, pk):
        try:
            task = Task.objects.filter(pk=pk).first()
            if not task:
                return Response({"error": "Task not found"}, status=404)

            self.check_object_permissions(request, task)

            serializer = TaskSerializer(task, data=request.data, partial=True)

            with transaction.atomic():
                if serializer.is_valid():
                    serializer.save(owner=task.owner)
                    return Response(serializer.data)

                return Response(serializer.errors, status=400)

        except Exception as e:
            return Response(
                {"error": "Failed to update task", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TaskDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def delete(self, request, pk):
        try:
            task = Task.objects.filter(pk=pk).first()
            if not task:
                return Response({"error": "Task not found"}, status=404)

            self.check_object_permissions(request, task)

            with transaction.atomic():
                task.delete()

            return Response({"message": "Task deleted successfully"}, status=204)

        except Exception as e:
            return Response(
                {"error": "Failed to delete task", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
