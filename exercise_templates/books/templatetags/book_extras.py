from django import template
from django.db.models import Avg, Count

from books.models import Book

register = template.Library()


@register.simple_tag
def recent_books():
    return Book.objects.order_by("-publishing_date", "-pk")[:3]


@register.inclusion_tag("books/_featured_books.html")
def featured_books(count=3):
    books = Book.objects.annotate(
        average_rating=Avg("reviews__rating"), review_count=Count("reviews")
    ).filter(review_count__gt=0).order_by("-average_rating", "title")[:count]
    return {"books": books}
