from moebot.driver.dmx import DmxDriver
from moebot.database import CocktailDb
from moebot.coordinator import Coordinator, MissingIngredients
from moebot.config import Config


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
    driver = DmxDriver(port='/dev/ttyUSB0')
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

    try:
        while True:
            search = input("Enter a drink: ")

            search_res = db.search(search)

            if not search_res:
                print("ERROR: Drink not found")
                continue

            if len(search_res) == 1:
                if not prompt_bool(f"Make '{search_res[0].name}'? (y/n): "):
                    continue
            else:
                index = prompt_choice("Which drink? ", [d.name for d in search_res], cancel=True)

                if index is not None:
                    try:
                        target = search_res[index]
                        print(f"Making {target}")
                        coordinator.make_drink(driver, target)
                    except MissingIngredients as e:
                        print("ERROR: Missing ingredients: " + ', '.join(e.ingredients))
                        if prompt_bool("Continue without them? (y/n): "):
                            coordinator.make_drink(driver, search_res[index], ignore_missing=True)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
