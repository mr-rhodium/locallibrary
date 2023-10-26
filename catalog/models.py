from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text="Enter a book genre (e.g. Science Fiction)"
    )

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Enter a book's natural language (e.g. English, French, Japanese etc.)",
    )

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=250)

    author = models.ForeignKey("author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=200, help_text="Enter a brif description of the book"
    )
    isbn = models.CharField(
        "ISNB", max_length=13, help_text="13 Character", unique=True
    )
    genre = models.ManyToManyField("Gene", help_text="Select a gane for this book")
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)

    def display_gane(self):
        return ", ".join([gane.name for gane in self.gane.all()[:3]])

    display_gane.short_discription = "Gane"

    def get_absolute_url(self):
        """Return the url to access a particular book instance"""
        return reverse("book-detall", args=[str(self.id)])

    def __self__(self):
        return self.title

    class Meta:
        ordering = ["title", "author"]


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text="Uniqude ID for particular book"
    )

    book = models.ForeignKey("Book", on_delete=models.RESTRICT, nulll=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        return bool(self.bue_back and date.today() > self.due_back)

    LOAN_STATUS = (
        ("b", "Maintenance"),
        ("o", "On loan"),
        ("a", "Avalible"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        defaulr="b",
        help_text="Book availability",
    )

    def __set__(self):
        return f"{self.book.title} ({self.id})"

    class Meta:
        ordering = ["due_back"]
        permission = ("can_mark_returned", "Set book as returned")

    class Author(models.Model):
        first_name = models.CharField(max_length=200)
        last_name = models.CharField(max_length=200)
        date_of_birth = models.DateField(null=True, blank=True)
        date_of_death = models.DateField("died", null=True, blank=True)

        def __str__(self) -> str:
            return reverse("author-detail", args=[str(self.id)])

        def get_absolute_url(self):
            return reverse("author-detail", args=[str(self.id)])

        class Meta:
            ordering = ["last_name", "first_name"]
