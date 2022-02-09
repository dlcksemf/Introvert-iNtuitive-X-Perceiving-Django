from rest_framework import serializers
from books.models import Books, LoanedBooks, Wishes, Applications


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model=Books
        fields=["cover_photo", "title", "writer",
    "translator", "publisher", "published_date",
    "ISBN", "story", "state", "book_num", "category_id"]


    def create(self, validated_data):
        title = validated_data["title"]
        writer = validated_data["writer"]
        publisher = validated_data["publisher"]
        ISBN = validated_data["ISBN"]
        state = validated_data["state"]
        cover_photo = validated_data.get("cover_photo", "")
        translator = validated_data.get("translator", "")
        published_date = validated_data.get("published_date", "")
        story = validated_data.get("story", "")
        category_id = validated_data.get("category_id", None)

        new_book = Books(cover_photo=cover_photo, title=title, writer=writer, publisher=publisher, ISBN=ISBN,
                         state=state, translator=translator, published_date=published_date, story=story, category_id=category_id)
        new_book.save()

        return new_book


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