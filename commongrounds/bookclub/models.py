from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True,)
    contributor = models.ForeignKey(
        'accounts.Profile', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.CharField(max_length=255)
    synopsis = models.TextField(blank=True)
    publication_year = models.IntegerField()
    available_to_borrow = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_year']

    def __str__(self):
        return self.title


class BookReview(models.Model):
    user_reviewer = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE, null=True, blank=True)
    anon_reviewer = models.TextField(blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        reviewer = self.user_reviewer or self.anon_reviewer
        return f"{reviewer} - {self.title}"


class Bookmark(models.Model):
    profile = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_bookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} bookmarked {self.book}"


class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(
        'accounts.Profile', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        borrower = self.borrower or self.name
        return f"{borrower} borrowed {self.book}"
