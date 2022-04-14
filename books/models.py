from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimestampedModel):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]


class Books(TimestampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    book_num = models.AutoField(primary_key=True)
    # integerfield 어떻게 쓰는지 확인

    cover_photo = ProcessedImageField(upload_to='books/%Y/%M',
                                      blank=True,
                                      # processors=[ResizeToFill(512, 512)],
                                      format='JPEG',
                                      options={'quality': 80})

    title = models.CharField(max_length=100, db_index=True)
    writer = models.CharField(max_length=100, db_index=True)
    translator = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100)
    published_date = models.DateField(blank=True, null=True)
    # 달력 DateField 나오게 하는 방법
    ISBN = models.CharField(max_length=20,db_index=True)
    story = models.TextField(blank=True)
    amount = models.IntegerField(default=1)

    state = models.CharField(
        max_length=1,
        choices=[
            ("A", "Available"),
            ("B", "Borrowed"),
            ("D", "Deleted"),
        ]
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-book_num"]
        verbose_name="도서"
        verbose_name_plural="도서 목록"


class LoanedBooks(models.Model):
    loan_num = models.AutoField(primary_key=True)

    loaned_date = models.DateField(auto_now_add=True)
    return_due_date = models.DateField()
    returned_date = models.DateField(blank=True, null=True)
    return_state = models.CharField(
        max_length=1,
        choices=[
            ("L", "Loaned"),
            ("E", 'Extended'),
            ("P", "Pending"),
            ("R", "Returned"),
            ("O", "Overdue"),
        ]
    )
    point = models.IntegerField(default=0)

    book_name = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='loaned_books')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["return_state"]
        verbose_name="도서 대출"
        verbose_name_plural="대출 도서 목록"


class Wishes(models.Model):
    wish_num = models.AutoField(primary_key=True)

    book_name = models.ForeignKey(Books, on_delete=models.CASCADE)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-wish_num"]
        verbose_name = "찜"
        verbose_name_plural = "찜 목록"


class Applications(TimestampedModel):
    application_num = models.AutoField(primary_key=True)

    title = models.CharField(max_length=100,db_index=True)
    writer = models.CharField(max_length=100,db_index=True)
    publisher = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=20, db_index=True)
    confirm_date=models.DateField(blank=True,null=True)
    state = models.CharField(
        max_length=1,
        choices=[
            ("P", "Pending"),
            ("O", "Order"),
            ("D", "Denied"),
        ]
    )

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-state"]
        verbose_name="도서 신청"
        verbose_name_plural="도서 신청 목록"

class Review(TimestampedModel):
    review_num=models.AutoField(primary_key=True)
    review_content=models.CharField(max_length=100,db_index=True)
    review_rate=models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(5),
        ]
    )

    book_name = models.ForeignKey(Books, on_delete=models.CASCADE,null=True)
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        ordering=["-review_num"]
        verbose_name="리뷰"
        verbose_name_plural="리뷰 목록"