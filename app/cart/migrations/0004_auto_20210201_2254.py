# Generated by Django 3.1.3 on 2021-02-02 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20210105_2248'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'get_latest_by': 'created'},
        ),
    ]
