# Generated by Django 2.0.2 on 2018-03-26 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_auto_20180228_0315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'ordering': ['-pk']},
        ),
    ]
