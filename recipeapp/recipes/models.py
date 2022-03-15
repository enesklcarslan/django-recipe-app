from django.db import models
from sqlalchemy import null

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    # quantity = models.CharField(max_length=20)
    # unit = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.name}"

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', blank=True)
    ingredients_list = models.TextField(null=True, blank=True)
    directions = models.TextField()
    # image = models.ImageField(upload_to='images/', blank=True, null=True)
    imageUrl = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name