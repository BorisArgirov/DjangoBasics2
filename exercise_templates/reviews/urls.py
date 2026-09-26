from django.urls import path, re_path

from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.review_list, name="review-list"),
    # RegEx accepts only positive integer primary keys.
    re_path(r"^(?P<pk>[1-9][0-9]*)/$", views.review_details, name="review-details"),
]
