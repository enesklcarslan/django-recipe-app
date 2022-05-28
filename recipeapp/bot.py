import os
import re
import sys

import django
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipeapp.settings")
django.setup()

from recipes.models import Ingredient, Recipe


# below function gives an array of ingredients
def get_recipe_ingredient_names(content):
    recipe_units = {
        "gram",
        "kg",
        "kilogram",
        "ml",
        "litre",
        "adet",
        "yemek kaşığı",
        "çorba kaşığı",
        "çay kaşığı",
        "parça",
        "tatlı kaşığı",
        "demet",
        "paket",
        "su bardağı" "çay bardağı" "fincan",
        "tepeleme çorba kaşığı",
        "silme çorba kaşığı",
        "tepeleme çay kaşığı",
        "silme çay kaşığı",
        "tepeleme tatlı kaşığı",
        "silme tatlı kaşığı",
        "tepeleme yemek kaşığı",
        "silme yemek kaşığı",
        "çimdik",
    }
    """
    a recipe ingredient starts with a number, followed by a space, followed by a recipe unit
    from the list above, and then a space, followed by the ingredient name
    """
    recipe_ingredient_regex = re.compile(
        r"^\d+\s+(?:" + "|".join(recipe_units) + r")\s+\w+"
    )
    """
    find all the recipe ingredients in the url and return only the ingredient names
    """
    recipe_ingredients = []
    recipe_ingredients_soup = BeautifulSoup(content, "html.parser")
    recipe_ingredients_list = recipe_ingredients_soup.find_all(
        "ul", class_="recipe-materials"
    )
    for ingredient_list in recipe_ingredients_list:
        for ingredient_item in ingredient_list.find_all("li"):
            ingredient_item_text = ingredient_item.text
            if recipe_ingredient_regex.match(ingredient_item_text):
                recipe_ingredient_unit_regex = re.compile(
                    r"(?:" + "|".join(recipe_units) + r")"
                )
                recipe_ingredient_unit_match = (
                    recipe_ingredient_unit_regex.search(ingredient_item_text)
                )
                recipe_ingredient_name = ingredient_item_text[
                    recipe_ingredient_unit_match.start() :
                ]
                recipe_ingredient_name = recipe_ingredient_name.replace(
                    recipe_ingredient_unit_match.group(), ""
                )
                recipe_ingredients.append(recipe_ingredient_name.strip())
    return recipe_ingredients


def get_recipe_ingredients_list(content):
    output = ""
    recipe_ingredients_soup = BeautifulSoup(content, "html.parser")
    recipe_ingredients_list = recipe_ingredients_soup.find_all(
        "li", itemprop="ingredients"
    )
    for ingredient_item in recipe_ingredients_list:
        output += ingredient_item.text + "\n"
    # trim the last newline
    output = output[:-1]
    return output


def get_recipe_name(content):
    recipe_name_soup = BeautifulSoup(content, "html.parser")
    recipe_name = recipe_name_soup.find("h1", class_="recipe-name")
    return recipe_name.text.strip().lower()


def get_recipe_directions(content):
    output = ""
    recipe_directions_soup = BeautifulSoup(content, "html.parser")
    recipe_directions_list = recipe_directions_soup.find_all(
        "ol", class_="recipe-instructions"
    )
    for direction_list in recipe_directions_list:
        for direction_item in direction_list.find_all("li"):
            output += direction_item.text + "\n"
    output = output[:-1]
    return output


def get_recipe_image(content):
    recipe_image_soup = BeautifulSoup(content, "html.parser")
    recipe_image_div = recipe_image_soup.find(
        "div", class_="recipe-single-img"
    )
    recipe_image_item = recipe_image_div.find("div", class_="item")
    recipe_image_url = recipe_image_item.find("img")["src"]
    return recipe_image_url


def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def main():
    with open("sample_recipes.txt", "r") as f:
        urls = f.read().splitlines()

    for url in urls:
        content = get_content(url)
        if not content:
            print("Not able to get data from the site. Check your URL.")
            return

        recipe_name = get_recipe_name(content)
        recipe_ingredients = get_recipe_ingredient_names(content)
        recipe_directions = get_recipe_directions(content)
        recipe_ingredients_list = get_recipe_ingredients_list(content)
        image_url = get_recipe_image(content)
        recipe = Recipe(
            name=recipe_name,
            directions=recipe_directions,
            ingredients_list=recipe_ingredients_list,
            imageUrl=image_url,
        )

        recipe.save()
        for ingredient in recipe_ingredients:
            ingredient_obj, _ = Ingredient.objects.get_or_create(
                name=ingredient
            )
            recipe.ingredients.add(ingredient_obj)
        recipe.save()
        print(f"{recipe_name} saved successfully")


if __name__ == "__main__":
    main()
