# Generated by Django 3.2.6 on 2021-08-26 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_my_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='my_field',
            field=models.CharField(choices=[('a', 'Anime'), ('b', 'Football'), ('c', 'Framework'), ('d', 'Other')], max_length=20, null=True),
        ),
    ]
