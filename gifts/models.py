from django.contrib.auth.models import User
from django.db import models


class GiftList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gift_lists")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)  # آیا این لیست برای دوستان قابل دیدن هست؟
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GiftItem(models.Model):
    gift_list = models.ForeignKey(GiftList, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='gift_items/', blank=True, null=True)
    reserved = models.BooleanField(default=False)  # وضعیت رزرو

    def __str__(self):
        return self.name

class Reservation(models.Model):
    item = models.OneToOneField(GiftItem, on_delete=models.CASCADE, related_name="reservation")
    reserved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.item.name} by {self.reserved_by.username}"

