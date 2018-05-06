import pkg_resources
import requests
import pint
import json
import os

import drink


UNIT_FILE = pkg_resources.resource_filename('moebot', 'data/units.txt')
ureg = pint.UnitRegistry()
ureg.load_definitions(UNIT_FILE)

Q = ureg.Quantity

# Search cocktail by name
# https://www.thecocktaildb.com/api/json/v1/1/search.php?s=margarita
# Search ingredient by name
# https://www.thecocktaildb.com/api/json/v1/1/search.php?i=vodka
# Lookup full cocktail details by id
# https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=13060
# Lookup a random cocktail
# https://www.thecocktaildb.com/api/json/v1/1/random.php
# Search by ingredient
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Gin
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Vodka
# Filter by alcoholic
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic
# Filter by Category
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Ordinary_Drink
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail
# Filter by Glass
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=Cocktail_glass
# https://www.thecocktaildb.com/api/json/v1/1/filter.php?g=Champagne_flute
# List the categories, glasses, ingredients or alcoholic filters
# https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list
# https://www.thecocktaildb.com/api/json/v1/1/list.php?g=list
# https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list
# https://www.thecocktaildb.com/api/json/v1/1/list.php?a=list

DRINK = 's'
INGREDIENT = 'i'
ID = 'i'

BASE = "https://www.thecocktaildb.com/api/json/v1/1"

URL_SEARCH = BASE + "/search.php"
URL_LOOKUP = BASE + "/lookup.php"
URL_FILTER = BASE + "filter.php"
URL_LIST = BASE + "/list.php"


class CocktailDb:
    def convert_drink(self, data):
        id = data.get("idDrink")
        name = data.get("strDrink")

        # Place sugar cube in old fashioned glass and saturate with bitters, add a dash of plain water. Muddle until dissolved.
        # Fill the glass with ice cubes and add whiskey.
        #
        # Garnish with orange twist, and a cocktail cherry.

        extras = []
        for line in data["strInstructions"].lower().split("\r\n"):
            if not line:
                continue

            if "ice" in line:
                extras.append(drink.Ice())

            if "orange" in line:
                extras.append(drink.Wedge("orange"))

            if "garnish" in line and "cherry" in line:
                extras.append(drink.Garnish("cherry"))

            # TODO And more...

        pours = []
        for i in range(1, 16):
            ingredient = data.get(f"strIngredient{i}")
            amt = data.get(f"strMeasure{i}")

            if ingredient and amt:
                pours.append((ingredient, ureg(amt).to('mL')))

        return drink.Drink(name, drink.Pour(*pours), *extras)

    def search(self, name):
        res = requests.get(URL_SEARCH, params={DRINK: name})
        data = res.json()
        print(json.dumps(data))

        return [self.convert_drink(d) for d in data['drinks']]

    def substitutes(self, ingredient):
        pass

if __name__ == "__main__":
    db = CocktailDb()

    res = db.search("old fashioned")

    for d in res:
        print(str(d))
