
from django.db import models

# Create your models here.
class medical(models.Model):
    name=models.CharField(max_length=25,null=True)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=5,decimal_places=2, null=True)
    expirydate =models.DateField()

    def __str__(self) :
        return self.name