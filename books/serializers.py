from django.contrib.auth import get_user_model
from rest_framework import serializers
from books.models import Books, LoanedBooks, Wishes, Applications

User = get_user_model()

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
        cover_photo = validated_data.get("cover_photo", None)
        translator = validated_data.get("translator", None)
        published_date = validated_data.get("published_date", None)
        story = validated_data.get("story", None)
        category_id = validated_data.get("category_id", None)

        new_book = Books(cover_photo=cover_photo, title=title, writer=writer, publisher=publisher, ISBN=ISBN,
                         state=state, translator=translator, published_date=published_date, story=story, category_id=category_id)
        new_book.save()

        return new_book


class LoanedBooksSerializer(serializers.ModelSerializer):
    return_due_date = serializers.DateField()
    returned_date = serializers.DateField(allow_null=True)
    return_state = serializers.CharField()

    class Meta:
        model = LoanedBooks
        fields =[
        "return_due_date",
        "returned_date",
        "return_state",
        "loan_num",
        "book_name",
        "email",
        ]
        depth = 1


class LoanedBooksCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanedBooks
        fields = "__all__"


class WishesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wishes
        fields="__all__"


class ApplicationsSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')

    class Meta:
        model=Applications
        fields="__all__"
