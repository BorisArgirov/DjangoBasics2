from django.db import models

# Create your models here.

class Pet(models.Model):
    name = models.CharField(max_length=30)
    personal_photo = models.URLField()
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        editable=False,
    )
    def save(self, *args, **kwargs):
        self.slug = f"{self.name}-{self.pk}"
        super().save(*args, **kwargs)
