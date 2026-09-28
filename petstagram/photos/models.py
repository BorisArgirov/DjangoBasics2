from django.db import models

from photos.validator import FileSizeValidator


# Create your models here.

class Photo(models.Model):
    photo = models.ImageField(
        validators=[
            FileSizeValidator(5),
        ]
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=30)
    tag_pets = models.ManyToManyField(
        to='pets.Pet',
    )
    date_of_publication = models.DateField(auto_now=True)

