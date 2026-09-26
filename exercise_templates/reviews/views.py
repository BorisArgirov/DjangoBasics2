from django.shortcuts import get_object_or_404, render
from django.utils import timezone

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
