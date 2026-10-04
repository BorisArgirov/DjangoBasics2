from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

import books
from books.forms import BookCreateForm, BookEditForm, BookDeleteForm, SearchForm
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
    search_form = SearchForm(request.GET or None)

    if request.GET and search_form.is_valid():
        books = books.filter(title__icontains=search_form.cleaned_data["query"])

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

def book_create(request):
    form = BookCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('books:landing-page')

    context = {
        'form':form
    }

    return render(request, 'books/create.html', context)


def book_edit(request, slug):
    book = get_object_or_404(Book, slug=slug)
    form = BookEditForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect('books:landing-page')

    context = {
        'form':form
    }

    return render(request, 'books/edit.html', context)


def book_delete(request, slug):
    book = get_object_or_404(Book, slug=slug)
    form = BookDeleteForm(instance=book)

    if request.method == 'POST':
        book.delete()
        return redirect('books:landing-page')

    context = {
        'form':form
    }

    return render(request, 'books/delete.html', context)