# Generated by Django 2.2.1 on 2019-05-25 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='closing_data',
            new_name='closing_date',
        ),
    ]
