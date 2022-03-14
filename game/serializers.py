from rest_framework import serializers

from game.models import Game, LoanedGame


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["game_num", "game_name", "player_num","play_time",
                  "level","game_rule","game_cover_photo"]

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