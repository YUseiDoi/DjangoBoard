# Generated by Django 2.2.20 on 2021-04-21 12:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0002_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'])], verbose_name='投稿画像'),
        ),
    ]
