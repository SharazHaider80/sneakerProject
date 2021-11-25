from django.db import models
import computed_property
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class vendors(models.Model):
    vendor_name = models.CharField(max_length=50)
    vendor_url = models.URLField(max_length=500,null=True,default=None)
    availability = models.BooleanField(null=True,default=False)
    def __str__(self):
        return self.vendor_name

class sneakers_data(models.Model):
    product_name = models.CharField(max_length=1000,null=True, default=None)
    product_type = models.CharField(max_length=1000,null=True, default=None)
    lowest_price = models.FloatField(max_length=100,null=True,default=None)
    average_price = computed_property.ComputedFloatField(null=True,max_length=100,compute_from='calculate_average')
    highest_price = models.FloatField(max_length=100,null=True,default=None)
    brand_name = models.CharField(max_length=1000,null=True,default=None)
    color = models.CharField(max_length=1000,null=True,default=None)
    designer = models.CharField(max_length=1000,null=True,default=None)
    category = models.CharField(max_length=1000, null=True, default=None)
    nick_name = models.CharField(max_length=1000,null=True,default=None)
    release_date = models.DateTimeField(null=True,default=None)
    release_year = models.IntegerField(null=True,default=None)
    slug = models.TextField(max_length=5000,null=True,default=None)
    description = models.TextField(max_length=5000,null=True,default=None)
    material = models.TextField(max_length=5000,null=True,default=None)
    product_placeholder = models.TextField(max_length=5000,null=True,default=None)
    sku = models.CharField(max_length=1000,null=True,default=None)
    images = models.JSONField(null=True, blank=True, default=list)
    vendor_id = models.ForeignKey(
        'sneaerksdata.vendors',
        on_delete=models.CASCADE,related_name="vendorsId",
    )

    def calculate_average(self):
        return (self.lowest_price + self.highest_price)/2
