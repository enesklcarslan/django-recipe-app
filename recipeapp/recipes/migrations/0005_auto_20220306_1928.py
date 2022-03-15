# Generated by Django 3.2.7 on 2022-03-06 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipe_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='image',
        ),
        migrations.AddField(
            model_name='recipe',
            name='imageUrl',
            field=models.TextField(blank=True, null=True),
        ),
    ]