from django.db import models

# Create your models here.

class bizcircle(models.Model):
    city_id = models.IntegerField(null=False)
    city_name = models.CharField(max_length=20, null=False,)
    bizcircle_id = models.IntegerField(null=False, unique=True)
    bizcircle_name = models.CharField(max_length=50, null=False)

class project(models.Model):
    build_name =  models.CharField(max_length=50, null=False)
    build_addr =  models.CharField(max_length=100, null=False)
    open_time = models.DateTimeField(null=False)
    price = models.FloatField(null=False)
    desc =  models.CharField(max_length=255)
    building_count = models.IntegerField(null=False)
    house_amount = models.IntegerField(null=False)
    bizcircle = models.ForeignKey(bizcircle, on_delete=models.CASCADE)

class room(models.Model):
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    show_price = models.FloatField(null=False)
    frame_area = models.FloatField(null=False)

class order(models.Model):
    room = models.ForeignKey(room, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=20, null=False, unique=True)
    final_price = models.FloatField(null=False)
    sign_time = models.DateTimeField(null=False)
    city_id = models.IntegerField(null=False, default=0)


