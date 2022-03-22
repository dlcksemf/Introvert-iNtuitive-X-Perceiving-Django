from django.contrib import admin

from game.models import Game, LoanedGame, GameReview


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["game_num","game_name","player_num","play_time","level","game_rule"]

@admin.register(LoanedGame)
class LoanedGameAdmin(admin.ModelAdmin):
    list_display = ["loan_game_num","loaned_time","return_due_time","returned_time","return_state","user_id","game_name"]

@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ["game_review_num", "user_id", "game_review_content", "game_review_rate", "game_name",]