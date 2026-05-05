from django import forms
from .models import BookReview, Book, Borrow


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['title', 'comment']


class BookReviewAnonForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['anon_reviewer', 'title', 'comment']


class BookContributeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis',
                  'publication_year', 'available_to_borrow']


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'synopsis',
                  'publication_year', 'available_to_borrow']


class BookBorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['name', 'date_borrowed']


class BookFormFactory:
    @classmethod
    def get_form(cls, context, user=None):
        if context == 'review':
            class ReviewForm(BookReviewForm):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    if user and user.is_authenticated:
                        self.fields['user_reviewer'] = forms.CharField(
                            initial=user.profile.display_name,
                            disabled=True,
                            required=False
                        )
            return ReviewForm

        elif context == 'contribute':
            class ContributeForm(BookContributeForm):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    if user and user.is_authenticated:
                        self.fields['contributor'] = forms.CharField(
                            initial=user.profile.display_name,
                            disabled=True,
                            required=False
                        )
            return ContributeForm

        elif context == 'update':
            return BookUpdateForm

        else:
            raise ValueError(f"Unknown form context: '{context}'")
