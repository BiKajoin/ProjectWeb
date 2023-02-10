from djongo import models

# Create your models here.
class pvcellData(models.Model):
    _id = models.BigAutoField(primary_key = True)
    datetime = models.DateTimeField()
    w = models.FloatField(null = False, default = 0)
