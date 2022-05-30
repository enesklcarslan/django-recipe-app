import random

from django.db.models import Count, Subquery
from django.shortcuts import get_object_or_404, render

from .models import Ingredient, Recipe


# Create your views here.
def index(request):
    if request.method == 'POST' and request.POST.get('ingredients'):
        selected_ingredients = set(
            ingredient.strip() 
            for ingredient in request.POST.get('ingredients').split(',')
        )

        relevant_recipes = Recipe.objects.filter(
            id__in=Subquery(
                Recipe.objects.filter(
                    ingredients__name__in=selected_ingredients
                )
                .values("id")
                .alias(cnt=Count("id"))
                .filter(cnt__gte=len(selected_ingredients))
                )
            )


        context = {
            'relevant_recipes' : relevant_recipes,
            'ingredients' : Ingredient.objects.all()
        }
        return render(request, 'recipes.html', context)
    
    all_ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.order_by("?")
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
