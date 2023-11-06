# Generated by Django 4.2.7 on 2023-11-06 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ressourcemap', '0003_rename_ressource_recipeingredient_resource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='ressourcemap.ressource'),
        ),
    ]
