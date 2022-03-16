from rest_framework import serializers

from game.models import Game, LoanedGame


class GameListingField(serializers.RelatedField):
    def to_representation(self, value):
        loaned_time = value.loaned_time
        return_due_time = value.return_due_time
        returned_time=value.returned_time
        return_state = value.return_state

        return {
            "loaned_time": loaned_time,
            "return_due_time": return_due_time,
            "returned_time":returned_time,
            "return_state": return_state
        }

class GameSerializer(serializers.ModelSerializer):
    loaned_game = GameListingField(many=True, read_only=True)
    class Meta:
        model = Game
        fields = ["game_num", "game_name", "player_num","play_time",
                  "level","game_rule","game_cover_photo","game_state","loaned_game"]

class LoanedGameSerializer(serializers.ModelSerializer):
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