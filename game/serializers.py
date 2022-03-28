from rest_framework import serializers

from books.serializers import UserListingField
from game.models import Game, LoanedGame, GameReview


class GameListingField(serializers.RelatedField):
    def to_representation(self, value):
        game_name = value.game_name

        return game_name


class GameReviewField(serializers.RelatedField):
    def to_representation(self, value):
        game_review_num=value.game_review_num
        game_review_content=value.game_review_content
        game_review_rate=value.game_review_rate
        user_id=value.user_id.username
        created_at = value.created_at
        updated_at = value.updated_at

        return {
            "game_review_num":game_review_num,
            "game_review_content":game_review_content,
            "game_review_rate":game_review_rate,
            "user_id":user_id,
            "created_at": created_at,
            "updated_at": updated_at,
        }

class LoanedGameSerializer(serializers.ModelSerializer):
    game_name = GameListingField(read_only=True)
    user_id = UserListingField(read_only=True)

    class Meta:
        model=LoanedGame
        fields=[
            "loan_game_num",
            "loaned_time",
            "return_due_time",
            "returned_time",
            "return_state",
            "user_id",
            "game_name",
        ]

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


class GameReviewSerializer(serializers.ModelSerializer):
    game_name=GameListingField(read_only=True)
    user_id=UserListingField(read_only=True)

    class Meta:
        model=GameReview
        fields=["game_review_num","game_review_content","game_review_rate","user_id","game_name","updated_at"]

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


class GameSerializer(serializers.ModelSerializer):
    loaned_game = LoanedGameSerializer(many=True, read_only=True)
    gamereview_set = GameReviewSerializer(many=True,read_only=True)

    class Meta:
        model = Game
        fields = ["game_num", "game_name", "player_num","play_time",
                  "level","game_rule","game_cover_photo","game_state","loaned_game","gamereview_set"]


class LoanedGameCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=LoanedGame
        fields=["return_due_time","return_state","user_id","game_name"]

    def create(self, validated_data):
        loaned_game = LoanedGame.objects.create(**validated_data)
        loaned_game.game_return_state = "L"
        loaned_game.save()

        game = validated_data["game_name"]

        game.game_state = "B"
        game.save()

        return loaned_game

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        game = instance.game_name

        if validated_data["return_state"] == "R":
            game.game_state = "A"
            game.save()

        return instance


class GameReviewCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model=GameReview
        fields=["game_review_num","game_review_content","game_review_rate","user_id","game_name"]