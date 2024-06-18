from django.db import models

class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    travel_company = models.TextField()
    area = models.TextField()
    title = models.TextField()
    price = models.IntegerField(null=True)
    date = models.TextField()
    departure_city = models.TextField()
    duration = models.IntegerField(null=True)
    remaining_quota = models.TextField()
    tour_schedule =models.TextField()
    url = models.TextField()

    class Meta:
        db_table = "Trip"

class User_save(models.Model):

    username = models.TextField()
    travel_company = models.TextField()
    area = models.TextField()
    title = models.TextField()
    price = models.IntegerField(null=True)
    date = models.TextField()
    departure_city = models.TextField()
    duration = models.IntegerField(null=True)
    remaining_quota = models.TextField()
    tour_schedule =models.TextField()
    url = models.TextField()

    class Meta:
        db_table = "User_save"
