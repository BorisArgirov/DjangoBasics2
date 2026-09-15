from django.db import models

import categories


# Create your models here.

class Note(models.Model):
    class PriorityChoices(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'

    title = models.CharField(max_length=200)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    priority = models.IntegerField(
        choices=PriorityChoices.choices,
        default=PriorityChoices.LOW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        related_name='notes',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.title}"

