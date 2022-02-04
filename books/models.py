from django.conf import settings
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Books(TimestampedModel):
    book_num = models.IntegerField(primary_key=True)
    # integerfield 어떻게 쓰는지 확인

    cover_photo = models.ImageField(blank=True)
    title = models.CharField(max_length=100, db_index=True)
    writer = models.CharField(max_length=100, db_index=True)
    translator = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100)
    published_date = models.DateField(blank=True)
    # 달력 DateField 나오게 하는 방법
    ISBN = models.CharField(max_length=20,db_index=True)
    story = models.TextField(blank=True)

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


class Loaned_books(models.Model):
    loan_num = models.IntegerField(primary_key=True)

    loaned_date = models.DateField(auto_now_add=True)
    return_due_date = models.DateField()
    returned_date = models.DateField()
    return_state = models.CharField(
        max_length=1,
        choices=[
            ("L", "Loaned"),
            ("R", "Register"),
            ("R", "Returned"),
            ("D", "Deleted"),
        ]
    )

    book_num = models.ForeignKey(Books, on_delete=models.CASCADE)
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-loan_num"]
        verbose_name="도서 대출"
        verbose_name_plural="대출 도서 목록"


class Wishes(models.Model):
    wish_num = models.IntegerField(primary_key=True)

    book_num = models.ForeignKey(Books, on_delete=models.CASCADE)
    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-wish_num"]
        verbose_name = "찜"
        verbose_name_plural = "찜 목록"


class Applications(TimestampedModel):
    application_num = models.IntegerField(primary_key=True)

    title = models.CharField(max_length=100,db_index=True)
    writer = models.CharField(max_length=100,db_index=True)
    publisher = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=20, db_index=True)
    state = models.CharField(
        max_length=1,
        choices=[
            ("P", "Pending"),
            ("O", "Order"),
            ("D", "Denied"),
        ]
    )

    email = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-application_num"]
        verbose_name="도서 신청"
        verbose_name_plural="도서 신청 목록"

