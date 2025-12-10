from django.db import models
# from .accounts import User

class Task(models.Model):
    STATUS_CHOICES = [
        ("incomplete", "Incomplete"),
        ("completed", "Completed"),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="incomplete"
    )

    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
