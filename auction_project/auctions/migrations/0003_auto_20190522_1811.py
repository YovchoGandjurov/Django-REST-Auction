# Generated by Django 2.2.1 on 2019-05-22 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20190522_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('C', 'Closed')], default='Open', max_length=50),
        ),
    ]