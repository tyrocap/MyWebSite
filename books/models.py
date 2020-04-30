from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
import uuid
#this is here for you to
# reference any user-related foreign key model connections
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    pass


class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    label = models.CharField(max_length=50, blank=True)  # bestseller|new|etc
    description = models.TextField(blank=True)
    image = models.CharField(max_length=300, blank=True)
    primary_isbn13 = models.CharField(max_length=50, blank=True)
    discount_price = models.FloatField(blank=True, null=True)
    preview_link_google = models.CharField(max_length=300, blank=True)
    page_count = models.IntegerField()
    average_rating = models.DecimalField(max_digits=6, decimal_places=1)
    rating_count = models.IntegerField()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_product_page', args=[str(self.id)])


class CustomUserProfile(models.Model):
    cu_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE)
    cu_wanttoread_book = models.ForeignKey(Book, on_delete=models.CASCADE)

    cu_book_id = models.CharField(max_length=255)
    cu_book_progress = models.IntegerField(default=0)
    cu_book_progress_note = models.CharField(max_length=300, default='')

    # Generally, a parameter passed to this get_absolute_url should be id of
    # a user, but since I could not access it at the time, I used book_id,
    # which  makes things confusing in the url, because template of that url
    # will have multiple books (due to loop) and the id of one.
    def get_absolute_url(self):
        return reverse('product_view', args=[str(self.cu_book_id)])