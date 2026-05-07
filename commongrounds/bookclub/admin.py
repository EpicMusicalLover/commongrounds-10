from django.contrib import admin
from .models import Genre, Book, BookReview, Bookmark, Borrow


class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ("name",)
    ordering = ("name",)


class BookAdmin(admin.ModelAdmin):
    search_fields = ("title", "author",)
    list_display = ("title", "author", "publication_year", "genre",)
    list_filter = ("genre", "publication_year",)
    ordering = ("-publication_year", )


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookReview)
admin.site.register(Bookmark)
admin.site.register(Borrow)
