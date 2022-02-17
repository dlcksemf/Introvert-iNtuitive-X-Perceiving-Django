from django.contrib.auth import get_user_model
from rest_framework import serializers

from books.models import Books, LoanedBooks, Wishes, Applications, Category

User = get_user_model()


class LoanedBooksSerializer(serializers.ModelSerializer):
    return_due_date = serializers.DateField()
    returned_date = serializers.DateField(allow_null=True)
    return_state = serializers.CharField()

    class Meta:
        model = LoanedBooks
        fields =[
            "loan_num",
            "return_due_date",
            "returned_date",
            "return_state",
            'loaned_date',

            "user_id",
            "book_name",
        ]
        depth = 1

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        book_name_representation = representation.pop('book_name')
        for key in book_name_representation:
            representation[key] = book_name_representation[key]

        return representation

    def to_internal_value(self, data):
        book_name_internal = {}
        for key in BooksSerializer.Meta.fields:
            if key in data:
                book_name_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['book_name'] = book_name_internal
        return internal


class BookListingField(serializers.RelatedField):
    def to_representation(self, value):
        loaned_date = value.loaned_date
        return_due_date = value.return_due_date
        returned_date = value.returned_date
        return_state = value.return_state

        return {
            "loaned_date": loaned_date,
            "return_due_date": return_due_date,
            "returned_date": returned_date,
            "return_state": return_state
        }


class BooksSerializer(serializers.ModelSerializer):
    # loaned_books = LoanedBooks.objects \
    #     .order_by('-loaned_date') \
    #     .distinct('loan_num') \
    #     .values_list('loaned_date', flat=True)
    loaned_books = BookListingField(many=True, read_only=True)

    class Meta:
        model=Books
        fields=["book_num", "cover_photo", "title", "writer",
    "translator", "publisher", "published_date",
    "ISBN", "story", "state", "category", "loaned_books"]

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


class CategorySerializer(serializers.ModelSerializer):
    books_set = BooksSerializer(many=True)

    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        books_data = validated_data.pop('books_set')
        category = Category.objects.create(**validated_data)
        for book_data in books_data:
            Books.objects.create(category=category, **book_data)
        return category


class CategoryCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LoanedBooksCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanedBooks
        fields = "__all__"


class WishesCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wishes
        fields=["wish_num", "user_id", "book_name"]


class WishesSerializer(serializers.ModelSerializer):
    book_name = BooksSerializer(read_only=True)

    class Meta:
        model=Wishes
        fields=["wish_num", "user_id", "book_name"]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        book_name_representation = representation.pop('book_name')
        for key in book_name_representation:
            representation[key] = book_name_representation[key]

        return representation

    def to_internal_value(self, data):
        book_name_internal = {}
        for key in BooksSerializer.Meta.fields:
            if key in data:
                book_name_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['book_name'] = book_name_internal
        return internal


class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = "__all__"
