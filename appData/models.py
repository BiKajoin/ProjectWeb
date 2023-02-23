from djongo import models

# Create your models here.
class PVCellData (models.Model):
    _id = models.BigAutoField(primary_key = True, null = False)
    datetime = models.DateTimeField()
    year = models.IntegerField(null = False, default = 0)
    month = models.IntegerField(null = False, default = 0)
    day = models.IntegerField(null = False, default = 0)
    hour = models.IntegerField(null = False, default = 0)
    minute = models.IntegerField(null = False, default = 0)
    second = models.IntegerField(null = False, default = 0)
    Irradiance = models.FloatField(null = False, default = 0)
    Tm = models.FloatField(null = False, default = 0)
    Vdc = models.FloatField(null = False, default = 0)
    Idc = models.FloatField(null = False, default = 0)
    kWdc = models.FloatField(null = False, default = 0)
    kWhdc = models.FloatField(null = False, default = 0)
    Iac = models.FloatField(null = False, default = 0)
    Vln = models.FloatField(null = False, default = 0)
    VA = models.FloatField(null = False, default = 0)
    W = models.FloatField(null = False, default = 0)
    Var = models.FloatField(null = False, default = 0)
    pf = models.FloatField(null = False, default = 0)
    Hz = models.FloatField(null = False, default = 0)
    VAh = models.FloatField(null = False, default = 0)
    Whac = models.FloatField(null = False, default = 0)
    cloud_cover = models.FloatField(null = False, default = 0)


