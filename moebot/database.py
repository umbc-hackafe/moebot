import pkg_resources
import functools
import requests
import pint
import json
import os
import re

from moebot.drink import Drink, Pour, Ice, Wedge, Garnish


UNIT_FILE = pkg_resources.resource_filename('moebot', 'data/units.txt')
ureg = pint.UnitRegistry()
ureg.load_definitions(UNIT_FILE)

Q = ureg.Quantity


# @context bartending = bar
#    [mass] -> [volume]: value * (fluid_ounce / ounce)
# @end


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
URL_FILTER = BASE + "/filter.php"
URL_LIST = BASE + "/list.php"


blind_repl = {
    "fl oz": "floz",
    "fluid oz": "floz",
    "fluid ounce": "floz",
    "fl ounce": "floz",
}

mixed_number_re = re.compile(r'([0-9.]+)(\s+([0-9 /]+))?([A-Za-z ]+)')
oz_re = re.compile(r'\b(oz|ounce)')


def cleanup_amt(amt):
    unit_matches = re.findall(mixed_number_re, amt)

    if unit_matches:
        match = unit_matches[0]
        whole, _, frac, unit = match

        whole = float(whole.strip())
        frac = frac.strip()
        unit = unit.strip()

        if frac:
            num_str, denom_str = frac.split('/')
            num, denom = int(num_str), int(denom_str)

            amt = f"{whole+num/denom} {unit}"
        else:
            amt = f"{whole} {unit}"

    for search, repl in blind_repl.items():
        if search in amt:
            amt = amt.replace(search, repl)

    amt = re.sub(oz_re, 'floz', amt)

    return amt


class CocktailDb:
    def convert_drink(self, data):
        id = data.get("idDrink")
        name = data.get("strDrink")

        extras = []
        for line in data["strInstructions"].lower().split("\r\n"):
            if not line:
                continue

            if "ice" in line:
                extras.append(Ice())

            if "orange" in line:
                extras.append(Wedge("orange"))

            if "garnish" in line and "cherry" in line:
                extras.append(Garnish("cherry"))

            # TODO And more...

        pours = []
        for i in range(1, 16):
            ingredient = (data.get(f"strIngredient{i}") or "").strip().lower()
            amt = (data.get(f"strMeasure{i}") or "").strip().lower()

            if ingredient and amt:
                amt = cleanup_amt(amt)
                try:
                    n_amt = ureg(amt)
                except pint.UndefinedUnitError:
                    print(f"WARN: Unknown unit in quantity '{amt}' of '{ingredient}'")
                    continue

                if isinstance(n_amt, (int, float)) \
                    or n_amt.dimensionality != ureg.liter.dimensionality:
                    # Don't know what do do about things that are dimensionless
                    continue

                n_amt = n_amt.to('mL').magnitude
                pours.append((ingredient, n_amt))

        return Drink(name, Pour(*pours), *extras)

    @functools.lru_cache(100)
    def search(self, name):
        res = requests.get(URL_SEARCH, params={DRINK: name})
        data = res.json()

        return [self.convert_drink(d) for d in data.get('drinks') or ()]

    def all_drinks(self):
        res = requests.get(URL_LIST, params={'c': 'list'})
        data = res.json()
        categories = [v["strCategory"] for v in data["drinks"]]

        ids = set()

        for cat in categories:
            res = requests.get(URL_FILTER, params={'c': cat})
            data = res.json()

            for drink in data['drinks']:
                ids.add(int(drink['idDrink']))

            print(f"Found {len(ids)} drinks")

    def substitutes(self, ingredient):
        return []


class LocalDb:
    def __init__(self, config):
        self.drinks = [
            Drink("Self Test", Pour(*((ing, 30) for ing in config.slots)))
        ]
        self.config = config

    def search(self, name):
        return [drink for drink in self.drinks if name.lower().strip() in drink.name.lower()]


class AggregateDb:
    def __init__(self, *dbs):
        self.dbs = dbs

    def search(self, name):
        return sum((db.search(name) for db in self.dbs), [])

    def substitutes(self, ingredient):
        return sum((db.substitutes(ingredient) for db in self.dbs), [])

if __name__ == "__main__":
    db = CocktailDb()
    db.all_drinks()
