# Generated by Django 4.2.7 on 2023-11-10 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ressourcemap', '0002_alter_ressource_ressource_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='ressource',
            name='is_crafted',
            field=models.BooleanField(default=False),
        ),
    ]