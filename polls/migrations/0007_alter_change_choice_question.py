# Generated by Django 3.2.6 on 2021-10-13 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_change_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question'),
        ),
    ]