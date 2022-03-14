from django.contrib import admin

from game.models import Game, LoanedGame


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["game_num","game_name","player_num","play_time","level","game_rule"]

@admin.register(LoanedGame)
class LoanedGameAdmin(admin.ModelAdmin):
    list_display = ["loan_game_num","laned_time","return_due_time","returned_time","return_state","user_id","game_name"]