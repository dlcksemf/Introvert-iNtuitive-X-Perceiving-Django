from rest_framework import serializers
from books.models import Books, LoanedBooks, Wishes, Applications


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model=Books
        fields=["cover_photo", "title", "writer",
    "translator", "publisher", "published_date",
    "ISBN", "story", "state"]

class LoanedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanedBooks
        fields = "__all__"

class WishesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wishes
        fields="__all__"

class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Applications
        fields="__all__"