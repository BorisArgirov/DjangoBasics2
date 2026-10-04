from django.urls import include, path

from books import views

app_name = "books"

# The books/ prefix is shared by both nested routes.
book_patterns = [
    path('create/', views.book_create, name='create'),
path('<slug:slug>/edit/', views.book_edit, name='edit'),
path('<slug:slug>/delete/', views.book_delete, name='delete'),
    path("", views.book_list, name="book-list"),
    path("<slug:slug>/", views.book_details, name="book-details"),
]

urlpatterns = [
    path("", views.landing_page, name="landing-page"),
    path("books/", include(book_patterns)),
]
