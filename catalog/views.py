from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_require
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import RenewBookForm
from .models import Book, Author, BookInstance, Genre


def index(request):
    """
    View function for home page of site.
    """
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.count()

    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    return render(
        request,
        "index.html",
        context={
            "num_books": num_books,
            "num_instances": num_instances,
            "num_instances_available": num_instances_available,
            "num_authors": num_authors,
            "num_visits": num_visits,
        },
    )


class BookListView(generic.ListView):
    models = Book
    paginate_by = 50


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 50


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(PendingDeprecationWarning, generic.ListView):
    model = BookInstance
    permission_required = "catalog.can_mark_returned"
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Any]:
        return BookInstance.objects.filter(status__exact="o").order_by("due_back")


@login_required
@permission_require("catalog.can_mark_returned", raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.bue_beak = form.cleaned_data["renewal_date"]
            book_instance.save()

            return HttpResponseRedirect(reverse("all-borrowed"))
    else:
        proposed_renewel_date = datetime.date.today() + datetime.timedelta(weeks=2)
        form = RenewBookForm(initial={"renewel_date": proposed_renewel_date})
    context = {
        "form": form,
        "book_instance": book_instance,
    }

    return render(request, "catalog/book_renew_librarian.html", context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = "__all__"
    initial = {"date_of_death": "01/01/2023"}
    permission_required = "catalog.can_mark_returned"


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = "__all__"
    permission_required = "catalog.can_mark_returned"


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy("authors")
    permission_required = "catalog.can_mark_returned"


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = "__all__"
    permission_required = "catalog.can_mark_returned"


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = "__all__"
    permission_required = "catalog.can_mark_returned"


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy("books")
    permission_required = "catalog.can_mark_returned"
