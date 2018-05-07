from moebot.driver.dmx import DmxDriver
from moebot.database import CocktailDb
from moebot.coordinator import Coordinator, MissingIngredients
from moebot.config import Config
from moebot.drink import Drink, Pour

def prompt_bool(text):
    while True:
        res = input(text)
        if res.lower().startswith('y'):
            return True
        elif res.lower().startswith('n'):
            return False


def prompt_choice(text, choices, cancel=False):
    print("=" * (max((len(s) for s in choices)) + 1))

    for i, choice in enumerate(choices):
        print(f"[ {i+1: >2d} ] : {choice}")

    if cancel:
        print("[  Q ] : Cancel")

    print("=" * (max((len(s) for s in choices)) + 1))

    res = 0
    while not (1 <= res <= len(choices)):
        raw_res = input(text)

        if cancel and raw_res.lower().startswith('q'):
            return None

        try:
            res = int(raw_res)
        except ValueError:
            print("Invalid input")

    return res - 1


def main():
    driver = DmxDriver(port='/dev/ttyUSB0', offset=13)
    db = CocktailDb()
    config = Config([
        "vodka",
        "whiskey",
        "aromatic bitters",
        "bourbon",
        "gin",
        "triple sec",
        "grenadine",
        "vermouth",
    ])
    coordinator = Coordinator(config)

    test_drink = Drink("Self Test", Pour(*((ing, 100) for ing in config.slots)))

    local_drinks = [test_drink]

    try:
        while True:
            search = input("Enter a drink: ")

            search_res = db.search(search) \
                + [drink for drink in local_drinks if search.lower().strip() in drink.name.lower()]

            if not search_res:
                print("ERROR: Drink not found")
                continue

            target = None
            if len(search_res) == 1:
                if not prompt_bool(f"Make '{search_res[0].name}'? (y/n): "):
                    continue
                target = search_res[0]
            else:
                index = prompt_choice("Which drink? ", [d.name for d in search_res], cancel=True)

                if index is not None:
                    target = search_res[index]

            try:
                print(f"Making {target}")
                coordinator.make_drink(driver, target)
            except MissingIngredients as e:
                print("ERROR: Missing ingredients: " + ', '.join(e.ingredients))
                if prompt_bool("Continue without them? (y/n): "):
                    coordinator.make_drink(driver, target, ignore_missing=True)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
