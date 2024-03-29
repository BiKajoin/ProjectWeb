# Generated by Django 4.1.6 on 2023-02-21 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appData', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pvcelldata',
            old_name='w',
            new_name='Hz',
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Iac',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Idc',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Irradiance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Tm',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='VA',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='VAh',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Var',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Vdc',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Vln',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='W',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='Whac',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='cloud_cover',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='day',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='hour',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='kWdc',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='kWhdc',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='minute',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='pf',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='second',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pvcelldata',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
