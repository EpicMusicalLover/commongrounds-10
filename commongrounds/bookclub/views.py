from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from datetime import date, timedelta
from .models import Book, Bookmark, Borrow, BookReview
from .forms import BookBorrowForm, BookFormFactory
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books = Book.objects.all()
        user = self.request.user

        if user.is_authenticated:
            profile = user.profile

            contributed = all_books.filter(contributor=profile)
            bookmarked = all_books.filter(bookmark__profile=profile)
            reviewed = all_books.filter(bookreview__user_reviewer=profile)

            contributed_ids = [book.pk for book in contributed]
            bookmarked_ids = [book.pk for book in bookmarked]
            reviewed_ids = [book.pk for book in reviewed]

            user_book_ids = contributed_ids + bookmarked_ids + reviewed_ids

            context['all_books'] = all_books.exclude(pk__in=user_book_ids)

            context['contributed_books'] = contributed
            context['bookmarked_books'] = bookmarked
            context['reviewed_books'] = reviewed
            context['all_books'] = all_books.exclude(pk__in=user_book_ids)

        else:
            context['all_books'] = all_books

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        user = self.request.user

        ReviewForm = BookFormFactory.get_form("review", user=self.request.user)
        context['review_form'] = ReviewForm()
        context['reviews'] = BookReview.objects.filter(book=book)
        context['bookmark_count'] = Bookmark.objects.filter(book=book).count()

        if user.is_authenticated:
            context['is_contributor'] = (book.contributor == user.profile)
            context['is_bookmarked'] = Bookmark.objects.filter(
                book=book, profile=user.profile).exists()

        return context

    def post(self, request, *args, **kwargs):
        book = self.get_object()

        if request.POST.get('action') == 'bookmark':
            if not request.user.is_authenticated:
                return redirect('login')

            profile = request.user.profile
            existing = Bookmark.objects.filter(book=book, profile=profile)

            if existing.exists():
                existing.delete()
            else:
                Bookmark.objects.create(
                    book=book,
                    profile=profile,
                    date_bookmarked=date.today()
                )

            return redirect('bookclub:book_detail', pk=book.pk)

        ReviewForm = BookFormFactory.get_form("review", user=request.user)
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            if request.user.is_authenticated:
                review.user_reviewer = request.user.profile
            else:
                review.anon_reviewer = "Anonymous"
            review.save()

        return redirect('bookclub:book_detail', pk=book.pk)


class BookCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    template_name = "book_form.html"
    required_role = "Book Contributor"

    def get(self, request):
        FormClass = BookFormFactory.get_form("contribute", user=request.user)
        form = FormClass()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        FormClass = BookFormFactory.get_form("contribute", user=request.user)
        form = FormClass(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.contributor = request.user.profile
            book.save()
            return redirect('bookclub:book_detail', pk=book.pk)
        return render(request, self.template_name, {'form': form})


class BookUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Book
    template_name = "book_update_form.html"
    required_role = "Book Contributor"

    def get(self, request, pk):
        book = Book.objects.get(pk=pk)
        FormClass = BookFormFactory.get_form("update")
        form = FormClass(instance=book)
        return render(request, self.template_name, {'form': form, 'book': book})

    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        FormClass = BookFormFactory.get_form("update")
        form = FormClass(instance=book, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bookclub:book_detail', pk=pk)
        return render(request, self.template_name, {'form': form, 'book': book})


class BookBorrowView(UpdateView):
    template_name = "book_borrow.html"

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return render(request, '404.html', status=404)
        form = BookBorrowForm()
        return render(request, self.template_name, {'book': book, 'form': form})

    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return render(request, '404.html', status=404)
        form = BookBorrowForm(request.POST)

        if form.is_valid():
            date_borrowed = form.cleaned_data['date_borrowed']
            date_to_return = date_borrowed + timedelta(weeks=2)

            if request.user.is_authenticated:
                Borrow.objects.create(
                    book=book,
                    borrower=request.user.profile,
                    name=request.user.profile.display_name,
                    date_borrowed=date_borrowed,
                    date_to_return=date_to_return
                )
            else:
                Borrow.objects.create(
                    book=book,
                    name=form.cleaned_data['name'],
                    date_borrowed=date_borrowed,
                    date_to_return=date_to_return
                )

            book.available_to_borrow = False

            book.save()

            return redirect('bookclub:book_detail', pk=book.pk)

        return render(request, self.template_name, {'book': book, 'form': form})
