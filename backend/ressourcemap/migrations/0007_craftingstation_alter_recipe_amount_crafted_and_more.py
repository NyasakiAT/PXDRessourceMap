# Generated by Django 4.2.7 on 2023-11-06 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ressourcemap', '0006_recipe_amount_crafted_alter_recipe_processing_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='CraftingStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.AlterField(
            model_name='recipe',
            name='amount_crafted',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='crafting_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ressourcemap.craftingstation'),
        ),
    ]
