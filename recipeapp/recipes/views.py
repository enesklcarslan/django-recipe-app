from django.shortcuts import get_object_or_404, render
from .models import Recipe, Ingredient
from django.db.models import Count
import random

# Create your views here.
def index(request):
    if request.method == 'POST' and request.POST.get('ingredients'):
        selected_ingredients = set(request.POST.get('ingredients').split(','))
        print(selected_ingredients)
        # check if a recipe exists with ingredients that are a subset of the selected ingredients
        recipes = Recipe.objects.all()
        relevant_recipes = Recipe.objects.none()
        for recipe in recipes:
            recipe_ingredients = set(recipe.ingredients.values_list('name', flat=True))
            if recipe_ingredients.issubset(selected_ingredients):
                relevant_recipes = relevant_recipes | Recipe.objects.filter(id = recipe.id)

        context = {
            'relevant_recipes' : relevant_recipes,
            'ingredients' : Ingredient.objects.all()
        }
        return render(request, 'recipes.html', context)
    else:
        all_ingredients = Ingredient.objects.all()
        recipes = list(Recipe.objects.all())
        recipes = random.sample(recipes, 9) if len(recipes) > 9 else recipes
        context = {
            'recipes' : recipes,
            'ingredients' : all_ingredients,
        }

    return render(request, 'index.html', context)

def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients_list = recipe.ingredients_list.split('\n')
    ingredients = recipe.ingredients.all()
    directions_list = recipe.directions.split('\n')
    context = {
        'recipe' : recipe,
        'ingredients' : ingredients,
        'directions' : directions_list,
        'ingredients_list' : ingredients_list,
    }
    return render(request, 'recipe_details.html', context)