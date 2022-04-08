from django.contrib import admin

from books.models import Books, LoanedBooks, Wishes, Applications, Review


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ["book_num", "title", "writer", "publisher", "ISBN", "state"]


@admin.register(LoanedBooks)
class LoanedBooksAdmin(admin.ModelAdmin):
    list_display = ["loan_num", "loaned_date", "return_due_date", "returned_date", "return_state", "book_name", "user_id"]


@admin.register(Wishes)
class WishesAdmin(admin.ModelAdmin):
    list_display = ["wish_num", "book_name", "user_id"]


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ["application_num", "title", "writer", "publisher", "ISBN", "state", "user_id","created_at","confirm_date"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["review_num","user_id","review_content","review_rate","book_name","updated_at"]
