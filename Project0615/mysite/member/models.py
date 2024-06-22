from django.db import models


class Member(models.Model):

    username = models.CharField(max_length=50)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=50)
    verification = models.BooleanField()

    class Meta:

        db_table = "member"
