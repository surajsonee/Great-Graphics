from django.db import models


class Category(models.Model):
    """graphic categories"""
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Graphic(models.Model):
    """graphic fields"""
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    # name, description and price are not optional
    name = models.CharField(max_length=254)
    description = models.TextField()
    requirement = models.TextField(max_length=100, null=True, blank=True)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    has_orientation = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    size_choices = (
        ('a5', 'A5'),
        ('a4', 'A4'),
        ('a3', 'A3'),
        ('a2', 'A2'),
    )
    orientation_choices = (
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    )
    size = models.CharField(max_length=20, choices=size_choices, blank=True)
    orientation = models.CharField(max_length=20, choices=orientation_choices, blank=True)

    def __str__(self):
        return self.name
