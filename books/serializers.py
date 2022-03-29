from django.contrib.auth import get_user_model
from rest_framework import serializers

from books.models import Books, LoanedBooks, Wishes, Applications, Category, Review

User = get_user_model()


class UserListingField(serializers.RelatedField):
    def to_representation(self, value):
        user_id = value.user_id
        username = value.username
        birthdate = value.birthdate

        return {
            "user_id" : user_id,
            "username": username,
            "birthdate": birthdate
        }


class ReviewListingField(serializers.RelatedField):
    def to_representation(self, value):
        # loaned_date = value.loaned_date
        # return_due_date = value.return_due_date
        # return_state = value.return_state
        book_name=value.title



        return {
            # "loaned_date": loaned_date,
            # "return_due_date": return_due_date,
            # "return_state": return_state
            "book_name":book_name,
        }

class BookListingField(serializers.RelatedField):
    def to_representation(self, value):
        loaned_date = value.loaned_date
        return_due_date = value.return_due_date
        return_state = value.return_state




        return {
            "loaned_date": loaned_date,
            "return_due_date": return_due_date,
            "return_state": return_state,
        }



class LoanCount(serializers.RelatedField):
    def to_representation(self, value):
        loaned_date = value.loaned_date
        return_due_date = value.return_due_date
        return_state = value.return_state

        return {
            "loaned_date": loaned_date,
            "return_due_date": return_due_date,
            "return_state": return_state
        }

class ReviewField(serializers.RelatedField):
    def to_representation(self, value):
        review_num = value.review_num
        review_content = value.review_content
        review_rate = value.review_rate
        user_id = value.user_id.username
        created_at = value.created_at
        updated_at = value.updated_at

        return {
            "review_num": review_num,
            "review_content": review_content,
            "review_rate": review_rate,
            "user_id": user_id,
            "created_at": created_at,
            "updated_at": updated_at,
        }

class ReviewSerializer(serializers.ModelSerializer):
    book_name = ReviewListingField(read_only=True)
    user_id = UserListingField(read_only=True)
    # created_at = ReviewField

    class Meta:
        model = Review
        fields=["review_num","review_content","review_rate","user_id","book_name","created_at","updated_at"]

    def to_representation(self, obj):
        representation = super().to_representation(obj)

        # game_name_representation = representation.pop('game_name')
        # for key in game_name_representation:
        #     if (key != "loaned_game"):
        #         representation[key] = game_name_representation[key]

        user_id_representation = representation.pop('user_id')
        representation["user_id"] = user_id_representation["user_id"]
        representation["username"] = user_id_representation["username"]
        # representation["birthdate"] = user_id_representation["birthdate"]

        return representation


class BooksSerializer(serializers.ModelSerializer):
    loaned_books = BookListingField(many=True, read_only=True)
    count_loans = serializers.SerializerMethodField()
    return_due_date = serializers.SerializerMethodField()
    review_set = ReviewField(many=True, read_only=True)


    class Meta:
        model=Books
        fields=["book_num", "cover_photo", "title", "writer",
                "translator", "publisher", "published_date",
                "ISBN", "story", "state", "amount", "category", "loaned_books",
                "count_loans", "return_due_date", "review_set","created_at","updated_at"]

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

    def get_count_loans(self, instance):
        return instance.loaned_books.count()

    def get_return_due_date(self, instance):
        if instance.state == "B" or instance.state == "P":
            return instance.loaned_books.first().return_due_date


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


class LoanedBooksSerializer(serializers.ModelSerializer):
    book_name = BooksSerializer()
    user_id = UserListingField(read_only=True)

    class Meta:
        model = LoanedBooks
        fields = [
            "user_id",
            "book_name",

            "loan_num",
            "return_due_date",
            "returned_date",
            "return_state",
            'loaned_date',
        ]

    def to_representation(self, obj):
        representation = super().to_representation(obj)

        book_name_representation = representation.pop('book_name')
        for key in book_name_representation:
            if (key != "wishes_set" and key != "loaned_books"):
                representation[key] = book_name_representation[key]

        user_id_representation = representation.pop('user_id')
        print(user_id_representation)
        representation["user_id"] = user_id_representation["user_id"]
        representation["username"] = user_id_representation["username"]
        representation["birthdate"] = user_id_representation["birthdate"]

        return representation


class LoanedBooksCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanedBooks
        fields = ["return_due_date", "book_name", "user_id", "return_state"]

    def create(self, validated_data):
        loaned_books = LoanedBooks.objects.create(**validated_data)
        loaned_books.return_state = "L"
        loaned_books.save()

        book = validated_data["book_name"]

        book.state = "B"
        book.save()

        return loaned_books

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        book = instance.book_name

        if validated_data["return_state"] == "R":
            book.state = "A"
            book.save()

        return instance


class WishesCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wishes
        fields=["wish_num", "user_id", "book_name"]


class WishesSerializer(serializers.ModelSerializer):
    book_name = BooksSerializer(read_only=True)
    user_id = UserListingField(read_only=True)

    class Meta:
        model=Wishes
        fields=["wish_num", "user_id", "book_name"]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        book_name_representation = representation.pop('book_name')
        for key in book_name_representation:
            representation[key] = book_name_representation[key]

        user_id_representation = representation.pop('user_id')
        representation["user_id"] = user_id_representation["user_id"]
        representation["username"] = user_id_representation["username"]

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


class ReviewCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields=["review_num","review_content","review_rate","user_id","book_name"]
