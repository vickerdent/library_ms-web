# Generated by Django 4.2.2 on 2023-06-30 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='slug',
            field=models.CharField(default='djangodbmodelsfieldscharfield'),
        ),
    ]
