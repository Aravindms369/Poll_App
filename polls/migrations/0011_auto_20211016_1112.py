# Generated by Django 3.2.6 on 2021-10-16 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20211016_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote_count',
            name='question_voted',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vote_count',
            name='voter',
            field=models.IntegerField(default=0),
        ),
    ]
