# Generated by Django 3.1.5 on 2021-01-14 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20210114_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resizedimage',
            name='resized_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]