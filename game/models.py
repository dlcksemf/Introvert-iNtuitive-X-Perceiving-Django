from django.conf import settings
from django.db import models

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Game(TimestampedModel):
    game_num=models.AutoField(primary_key=True)
    game_name=models.CharField(max_length=50, db_index=True)
    player_num=models.CharField(max_length=10,db_index=True)
    play_time=models.CharField(max_length=10,db_index=True)
    level=models.CharField(max_length=10,db_index=True)
    game_rule=models.TextField(blank=True)
    game_state=models.CharField(
        max_length=1,
        default='A',
        choices=[
            ("A","Available"),
            ("B", "Borrowed"),
        ]
    )

    game_cover_photo=models.ImageField(
        upload_to="books/%Y/%M",
        blank=True
    )

    def __str__(self):
        return self.game_name

    class Meta:
        ordering=["-game_num"]
        verbose_name="게임"
        verbose_name_plural="게임 목록"

class LoanedGame(models.Model):
    loan_game_num=models.AutoField(primary_key=True)

    loaned_time=models.DateTimeField()
    return_due_time=models.DateTimeField()
    returned_time=models.DateTimeField()
    return_state=models.CharField(
        max_length=1,
        choices=[
            ("L","Loaned"),
            ("R","Returned"),
        ]
    )

    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    game_name=models.ForeignKey(Game,on_delete=models.CASCADE,related_name="loaned_game")

    class Meta:
        ordering=["-loan_game_num"]
        verbose_name="게임 대여"
        verbose_name_plural="대여 게임 목록"