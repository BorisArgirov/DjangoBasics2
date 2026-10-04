from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from reviews.forms import ReviewCreateForm, ReviewEditForm, ReviewDeleteForm
from reviews.models import Review


def review_list(request):
    reviews = Review.objects.select_related("book").order_by("-created_at", "-pk")[:10]
    context = {
        "page_title": "Recent reviews",
        "current_year": timezone.now().year,
        "reviews": reviews,
    }
    return render(request, "reviews/review_list.html", context)


def review_details(request, pk):
    review = get_object_or_404(Review.objects.select_related("book"), pk=pk)
    context = {
        "page_title": f"Review by {review.author}",
        "current_year": timezone.now().year,
        "review": review,
    }
    return render(request, "reviews/review_details.html", context)


def review_create(request):
    form = ReviewCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('books:book-list')

    context = {
        'form': form,
        'page_title': f'Create Review',
    }
    return render(request, "reviews/create.html", context)


def review_edit(request, pk: int):
    review = get_object_or_404(Review.objects.select_related("book"), pk=pk)
    form = ReviewEditForm(request.POST or None, instance=review)

    if form.is_valid():
        form.save()
        return redirect('book_list')

    context = {
        'form': form,
        'page_title': f'Edit Review',
    }
    return render(request, "reviews/edit.html", context)


def review_delete(request, pk: int):
    review = get_object_or_404(Review.objects.select_related("book"), pk=pk)
    form = ReviewDeleteForm(instance=review)

    if request.method == "POST":
        review.delete()
        return redirect('book_list')

    context = {
        'form': form,
        'page_title': f'Delete Review',
    }
    return render(request, "reviews/delete.html", context)
