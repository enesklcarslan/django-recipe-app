# Generated by Django 3.2.7 on 2022-03-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220306_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(blank=True, related_name='recipes', to='recipes.Ingredient'),
        ),
    ]
