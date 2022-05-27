from recipes.models import Recipe, Ingredient
from bs4 import BeautifulSoup
import requests
import re

#below function gives an array of ingredients
def get_recipe_ingredient_names(url):
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
        "su bardağı"
        "çay bardağı"
        "fincan",
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
    recipe_ingredient_regex = re.compile(r'^\d+\s+(?:' + '|'.join(recipe_units) + r')\s+\w+')
    """
    find all the recipe ingredients in the url and return only the ingredient names
    """
    recipe_ingredients = []
    recipe_ingredients_html = requests.get(url).text
    recipe_ingredients_soup = BeautifulSoup(recipe_ingredients_html, 'html.parser')
    recipe_ingredients_list = recipe_ingredients_soup.find_all('ul', class_='recipe-materials')
    for ingredient_list in recipe_ingredients_list:
        for ingredient_item in ingredient_list.find_all('li'):
            ingredient_item_text = ingredient_item.text
            if recipe_ingredient_regex.match(ingredient_item_text):
                recipe_ingredient_unit_regex = re.compile(r'(?:' + '|'.join(recipe_units) + r')')
                recipe_ingredient_unit_match = recipe_ingredient_unit_regex.search(ingredient_item_text)
                recipe_ingredient_name = ingredient_item_text[recipe_ingredient_unit_match.start():]
                recipe_ingredient_name = recipe_ingredient_name.replace(recipe_ingredient_unit_match.group(), '')
                recipe_ingredients.append(recipe_ingredient_name)
    return recipe_ingredients


def get_recipe_ingredients_list(url):
    output = ""
    recipe_ingredients_html = requests.get(url).text
    recipe_ingredients_soup = BeautifulSoup(recipe_ingredients_html, 'html.parser')
    recipe_ingredients_list = recipe_ingredients_soup.find_all('li', itemprop="ingredients")
    for ingredient_item in recipe_ingredients_list:
        output += ingredient_item.text + "\n"
    #trim the last newline
    output = output[:-1]
    return output

def get_recipe_name(url):
    recipe_name_html = requests.get(url).text
    recipe_name_soup = BeautifulSoup(recipe_name_html, 'html.parser')
    recipe_name = recipe_name_soup.find('h1', class_="recipe-name")
    return recipe_name.text

def get_recipe_directions(url):
    output = ""
    recipe_directions_html = requests.get(url).text
    recipe_directions_soup = BeautifulSoup(recipe_directions_html, 'html.parser')
    recipe_directions_list = recipe_directions_soup.find_all('ol', class_="recipe-instructions")
    for direction_list in recipe_directions_list:
        for direction_item in direction_list.find_all('li'):
            output += direction_item.text + "\n"
    output = output[:-1]
    return output

def get_recipe_image(url):
    recipe_image_html = requests.get(url).text
    recipe_image_soup = BeautifulSoup(recipe_image_html, 'html.parser')
    recipe_image_div = recipe_image_soup.find('div', class_="recipe-single-img")
    recipe_image_item = recipe_image_div.find('div', class_="item")
    recipe_image_url = recipe_image_item.find('img')['src']
    return recipe_image_url

def main():  
    url= input("Enter the url of the recipe: ")
    recipe_name = get_recipe_name(url)
    recipe_ingredients = get_recipe_ingredient_names(url)
    recipe_directions = get_recipe_directions(url)
    recipe_ingredients_list = get_recipe_ingredients_list(url)
    image_url = get_recipe_image(url)
    recipe = Recipe(name=recipe_name, directions=recipe_directions, ingredients_list=recipe_ingredients_list, imageUrl=image_url)
    recipe.save()
    for ingredient in recipe_ingredients:
        ingredient_obj = Ingredient.objects.get_or_create(name=ingredient)[0]
        recipe.ingredients.add(ingredient_obj)
    recipe.save()
    print(f"{recipe_name} saved successfully")

# if __name__ == "__main__":
#     main() -> Doesn't work while running from manage.py shell. No idea why.
try:
    while True:
        selection = input("Enter 1 to add a recipe, 2 to exit: ")
        if selection == "1":
            main()
        elif selection == "2":
            break
except:
    print("An error occured while trying to get the recipe")