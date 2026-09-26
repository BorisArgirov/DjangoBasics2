from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from books.models import Book
from reviews.models import Review


def landing_page(request):
    top_books = Book.objects.annotate(
        average_rating=Avg("reviews__rating"), review_count=Count("reviews")
    ).filter(review_count__gt=0).order_by("-average_rating", "title")[:3]
    context = {
        "page_title": "Home",
        "current_year": timezone.now().year,
        "top_books": top_books,
        "welcome_message": "Find your next <strong>great read</strong>.",
        "recent_reviews": Review.objects.select_related("book").order_by("-created_at", "-pk")[:3],
    }
    return render(request, "books/index.html", context)


def book_list(request):
    books = Book.objects.annotate(
        average_rating=Avg("reviews__rating"), review_count=Count("reviews")
    ).order_by("title")
    context = {
        "page_title": "All books",
        "current_year": timezone.now().year,
        "books": books,
    }
    return render(request, "books/book_list.html", context)


def book_details(request, slug):
    books = Book.objects.annotate(
        average_rating=Avg("reviews__rating"), review_count=Count("reviews")
    )
    book = get_object_or_404(books, slug=slug)
    context = {
        "page_title": book.title,
        "current_year": timezone.now().year,
        "book": book,
        "reviews": book.reviews.order_by("-created_at", "-pk"),
    }
    return render(request, "books/book_details.html", context)
