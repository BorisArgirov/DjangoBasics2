from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify


class Book(models.Model):
    class Genre(models.TextChoices):
        FICTION = "fiction", "Fiction"
        NON_FICTION = "non-fiction", "Non-Fiction"
        FANTASY = "fantasy", "Fantasy"
        SCIENCE = "science", "Science"
        MYSTERY = "mystery", "Mystery"
        ROMANCE = "romance", "Romance"
        OTHER = "other", "Other"

    title = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    isbn = models.CharField(
        max_length=12, unique=True, validators=[MinLengthValidator(12)]
    )
    genre = models.CharField(max_length=20, choices=Genre.choices)
    publishing_date = models.DateField()
    description = models.TextField()
    image_url = models.URLField()
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Tags(models.Model):
    name = models.CharField(max_length=50)
    book = models.ManyToManyField(Book)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name