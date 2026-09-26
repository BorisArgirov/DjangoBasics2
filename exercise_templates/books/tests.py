from datetime import date
from decimal import Decimal

from django.contrib.staticfiles import finders
from django.template import Context, Template
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from books.models import Book
from books.templatetags.book_extras import recent_books
from reviews.models import Review
from reviews.templatetags.review_extras import stars


class BookPagesTests(TestCase):
    def make_book(self, title="Test Book", number=1, published=None):
        return Book.objects.create(
            title=title, isbn=f"{number:012d}", price="12.50",
            genre=Book.Genre.FICTION,
            publishing_date=published or date(2024, 1, 1),
            description="", image_url="",
        )

    def test_empty_pages(self):
        for name in ("books:landing-page", "books:book-list", "reviews:review-list"):
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, str(timezone.now().year))
            self.assertTemplateUsed(response, "base.html")
        self.assertContains(self.client.get(reverse("books:book-list")), "0 books")

    def test_details_filters_and_missing_objects(self):
        book = self.make_book()
        review = Review.objects.create(book=book, author="Reader", body="<script>alert(1)</script>", rating="4.75")
        response = self.client.get(reverse("books:book-details", args=[book.slug]))
        for text in ("Top Rated", "1 Review", "12.500", "No description available.", "default-cover.svg", "****"):
            self.assertContains(response, text)
        self.assertNotContains(response, "<script>alert(1)</script>")
        self.assertContains(response, "&lt;script&gt;")
        detail = self.client.get(reverse("reviews:review-details", args=[review.pk]))
        self.assertContains(detail, "Reader")
        self.assertEqual(self.client.get("/books/not-found/").status_code, 404)
        self.assertEqual(self.client.get("/reviews/999999/").status_code, 404)
        self.assertEqual(self.client.get("/reviews/abc/").status_code, 404)

    def test_pages_reflect_added_and_removed_data(self):
        book = self.make_book()
        url = reverse("books:book-details", args=[book.slug])
        self.assertContains(self.client.get(url), "No reviews yet")
        review = Review.objects.create(book=book, author="Reader", body="Great book", rating="5.00")
        self.assertContains(self.client.get(url), "Top Rated")
        self.assertContains(self.client.get(reverse("books:landing-page")), "Test Book")
        review.delete()
        self.assertNotContains(self.client.get(url), "Top Rated")
        book.delete()
        self.assertContains(self.client.get(reverse("books:book-list")), "0 books")

    def test_rankings_and_recent_books(self):
        books = []
        for number in range(1, 5):
            book = self.make_book(f"Book {number}", number, date(2020 + number, 1, 1))
            Review.objects.create(book=book, author="Reader", body="A review", rating=number + 1)
            books.append(book)
        response = self.client.get(reverse("books:landing-page"))
        self.assertEqual(list(response.context["top_books"]), list(reversed(books[1:])))
        self.assertEqual(list(recent_books()), list(reversed(books[1:])))
        html = Template("{% load book_extras %}{% featured_books count=2 %}").render(Context())
        self.assertIn("Book 4", html)
        self.assertIn("Book 3", html)
        self.assertNotIn("Book 2", html)

    def test_recent_reviews_limit_and_order(self):
        book = self.make_book()
        reviews = [Review.objects.create(book=book, author=f"Reader {i}", body="A review", rating="4.00") for i in range(12)]
        response = self.client.get(reverse("reviews:review-list"))
        self.assertEqual(list(response.context["reviews"]), list(reversed(reviews))[:10])

    def test_custom_filter_and_static_assets(self):
        self.assertEqual(stars(Decimal("4.00")), "****")
        self.assertEqual(stars(None), "")
        self.assertEqual(stars("invalid"), "")
        self.assertIsNotNone(finders.find("books/images/default-cover.svg"))
        self.assertIsNotNone(finders.find("books/css/style.css"))
