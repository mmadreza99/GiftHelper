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


class GiftFund(models.Model):
    gift_item = models.OneToOneField(GiftItem, on_delete=models.CASCADE, related_name='fund')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_funded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fund for {self.gift_item.name}"

    def add_contribution(self, amount):
        """Method to add a contribution to the fund and update funding status."""
        self.current_amount += amount
        if self.current_amount >= self.target_amount:
            self.is_funded = True
        self.save()


class GiftContribution(models.Model):
    gift_fund = models.ForeignKey(GiftFund, on_delete=models.CASCADE, related_name='contributions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    contributed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contribution of {self.amount} by {self.user.username} to {self.gift_fund.gift_item.name}"

    def save(self, *args, **kwargs):
        """Override save to update fund's current amount."""
        super().save(*args, **kwargs)
        self.gift_fund.add_contribution(self.amount)


class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    gift_list = models.ForeignKey('GiftList', on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.title


class Comment(models.Model):
    gift_item = models.ForeignKey('GiftItem', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.gift_item.name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class GiftRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    gift_item = models.ForeignKey('GiftItem', on_delete=models.CASCADE, related_name='recommendations')
    reason = models.TextField(blank=True)

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.gift_item.name}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    gift_item = models.ForeignKey('GiftItem', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.user.username} for {self.gift_item.name} - {self.status}"
