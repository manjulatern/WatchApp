# Generated by Django 3.0.5 on 2020-04-25 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchapp', 'populate_auction_house'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='actual_lots',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='lot',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
