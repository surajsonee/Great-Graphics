import uuid

from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from graphics.models import Graphic
from profiles.models import UserProfile


class Order(models.Model):
    """customer order form"""
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total > settings.DISCOUNT_THRESHOLD:
            self.discount_amount = self.order_total * Decimal(settings.DISCOUNT_PERCENTAGE / 100)
        else:
            self.discount_amount = 0

        self.grand_total = self.order_total - self.discount_amount
        self.save()  # save instance

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """order line items"""
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    graphic = models.ForeignKey(Graphic, null=False, blank=False, on_delete=models.CASCADE)
    graphic_size = models.CharField(max_length=2, null=True, blank=True)  # A5, A4, A3, A2, A1
    graphic_orientation = models.CharField(max_length=10, null=True, blank=True)  # portrait, landscape
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
    if graphic_size == 'a5':
        factor = settings.POSTER_FACTOR_A5
    elif graphic_size == 'a4':
        factor = settings.POSTER_FACTOR_A5
    elif graphic_size == 'a3':
        factor = settings.POSTER_FACTOR_A5
    elif graphic_size == 'a2':
        factor = settings.POSTER_FACTOR_A5
    elif graphic_size == 'a1':
        factor = settings.POSTER_FACTOR_A5
    else:  # Default for icons and logos
        factor = 1.0

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.graphic.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.graphic.sku} on order {self.order.order_number}'
