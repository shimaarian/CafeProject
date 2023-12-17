from django.db import models
import datetime as dt
from django.contrib.auth import get_user_model
from django.urls import reverse
from taggit.managers import TaggableManager


user = get_user_model()


class ServingTime(models.Model):
    time = models.CharField(max_length=7)

    def __str__(self):
        return self.time


# class CategoryMenu(models.Model):
#     title = models.CharField(max_length=50)
#     serving_time = models.ManyToManyField(ServingTime)

class CategoryMenu(models.Model):
    title = models.CharField(max_length=50)

    serving_time = models.ManyToManyField(ServingTime)

    def __str__(self):
        return self.title


class Items(models.Model):
    category_id = models.ForeignKey(CategoryMenu, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    description = models.TextField(max_length=255)
    status = models.BooleanField()
    discount = models.PositiveIntegerField(default=0)
    number_items = models.PositiveIntegerField(default=1)
    like_count = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(user, through='Like', related_name='liked_item')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cafe:detail_item', args=[self.id])



class Order(models.Model):
    class OrderStatus(models.TextChoices):
        ORDER = "ORDER", "order"
        PAYMENT = "PAYMENT", "payment"
        CANCELED = "CANCELED", "Canceled"

    user = models.OneToOneField(user, on_delete=models.CASCADE, related_name="user_cart")
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.ORDER)
    order_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-order_time']
        indexes = [
            models.Index(fields=['-order_time'])
        ]

    def get_absolute_url(self):
        return reverse('cafe:cart-receipt', args=[user.id])
    def __str__(self):
        return f" {self.id}"


class OrderItem(models.Model):
    DoesNotExist = None
    number_items = models.PositiveIntegerField(default=1, blank=True)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True, default=0)
    delivery_time = models.TimeField(null=True, blank=True, default=dt.time(00, 00))
    items = models.ManyToManyField(Items, related_name="item_order")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")

    def __str__(self):
        return f"{self.order.id} "


class Receipt(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='receipt_order')

    class Meta:
        ordering = ['-time']
        indexes = [
            models.Index(fields=['-time'])
        ]

    def __str__(self):
        return f"{self.time}"


class Like(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, related_name="users")
    items = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="items")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{user.id}"
