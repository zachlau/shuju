# Generated by Django 2.1.4 on 2019-05-01 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='bizcircle',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.bizcircle'),
        ),
        migrations.AlterField(
            model_name='bizcircle',
            name='city_id',
            field=models.IntegerField(),
        ),
    ]
