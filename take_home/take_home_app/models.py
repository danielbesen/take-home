from django.db import models

class Account(models.Model):
    account_id = models.IntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=3)



    