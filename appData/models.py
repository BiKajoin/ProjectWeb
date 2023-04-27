from djongo import models
from django_tables2 import SingleTableView, Table, Column

# Create your models here.
class PVCellData (models.Model):
    datetime = models.DateTimeField(verbose_name="Timestamp")
    Irradiance = models.FloatField(verbose_name = "Irradiance (W/㎡)", null = False, default = 0)
    Tm = models.FloatField(verbose_name = "Temperature (℃)", null = False, default = 0)
    VA = models.FloatField(verbose_name = "Apparent Power (VA)", null = False, default = 0)
    W = models.FloatField(verbose_name = "Real Power (W)", null = False, default = 0)
    Var = models.FloatField(verbose_name = "Reactive Power (VAR)", null = False, default = 0)
    cloud_cover = models.FloatField(verbose_name = "Cloud Cover (Ratio)", null = False, default = 0)

    _id = models.BigAutoField(primary_key = True, null = False)
    year = models.IntegerField(null = False, default = 0)
    month = models.IntegerField(null = False, default = 0)
    day = models.IntegerField(null = False, default = 0)
    hour = models.IntegerField(null = False, default = 0)
    minute = models.IntegerField(null = False, default = 0)
    second = models.IntegerField(null = False, default = 0)
    Vdc = models.FloatField(null = False, default = 0)
    Idc = models.FloatField(null = False, default = 0)
    kWdc = models.FloatField(null = False, default = 0)
    kWhdc = models.FloatField(null = False, default = 0)
    Iac = models.FloatField(null = False, default = 0)
    Vln = models.FloatField(null = False, default = 0)
    pf = models.FloatField(null = False, default = 0)
    Hz = models.FloatField(null = False, default = 0)
    VAh = models.FloatField(null = False, default = 0)
    Whac = models.FloatField(null = False, default = 0)
    

class PVCellTable(Table):
    class Meta:
        model = PVCellData
        fields = ('datetime', 'Tm', 'Irradiance', 'VA', 'W', 'Var', 'cloud_cover')
        attrs = {"class": "table table-striped table-bordered"}