from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Game(TimestampedModel):
    game_num = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=50, db_index=True)
    player_num = models.CharField(max_length=10,db_index=True)
    play_time = models.CharField(max_length=10,db_index=True)
    level = models.CharField(max_length=10,db_index=True)
    game_rule = models.TextField(blank=True)
    game_state = models.CharField(
        max_length=1,
        default='A',
        choices=[
            ("A","Available"),
            ("B", "Borrowed"),
        ]
    )

    game_amount = models.IntegerField(default=1)

    game_cover_photo = ProcessedImageField(upload_to='books/%Y/%M',
                                           blank=True,
                                           processors=[ResizeToFill(512, 512)],
                                           format='JPEG',
                                           options={'quality': 80})

    def __str__(self):
        return self.game_name

    class Meta:
        ordering=["-game_num"]
        verbose_name="게임"
        verbose_name_plural="게임 목록"


class LoanedGame(models.Model):
    loan_game_num = models.AutoField(primary_key=True)
    loaned_time = models.DateTimeField(auto_now_add=True)
    return_due_time = models.DateTimeField()
    returned_time = models.DateTimeField(blank=True, null=True)
    return_state = models.CharField(
        max_length=1,
        choices=[
            ("L","Loaned"),
            ("R","Returned"),
        ]
    )

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    game_name = models.ForeignKey(Game,on_delete=models.CASCADE,related_name="loaned_game")

    class Meta:
        ordering = ["-loan_game_num"]
        verbose_name = "게임 대여"
        verbose_name_plural = "대여 게임 목록"


class GameReview(TimestampedModel):
    game_review_num = models.AutoField(primary_key=True)
    game_review_content = models.CharField(max_length=100,db_index=True)
    game_review_rate = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(5),
        ]
    )

    game_name = models.ForeignKey(Game,on_delete=models.CASCADE,null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    class Meta:
        ordering=["-game_review_num"]
        verbose_name="게임 리뷰"
        verbose_name_plural="게임 리뷰 목록"