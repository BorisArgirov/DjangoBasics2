from django.urls import path, re_path, include
from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.review_list, name="review-list"),
    # RegEx accepts only positive integer primary keys.
    re_path(r"^(?P<pk>[1-9][0-9]*)/$", views.review_details, name="review-details"),
    path('create/', views.review_create, name="create"),
    path('<int:pk>', include([
        path('', views.review_details, name="details"),
        path('delete/', views.review_delete, name="delete"),
        path('edit/', views.review_edit, name="edit"),
    ]))
]
