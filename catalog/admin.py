from django.contrib import admin
from .models import Author, Genre, Book, BorrowRequest, User

# Register your models here.

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BorrowRequest)
admin.site.register(User)
admin.site.register(Genre)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
    fields = ['first_name', 'last_name', ('date_of_birth')]


@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_date', 'id')
    list_filter = ('status', 'request_date', 'due_date')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'request_date', 'due_date', 'borrower')
        }),
    )

class BorrowRequestInline(admin.TabularInline):
    model = BorrowRequest

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre')
    inlines = [BorrowRequestInline]