from moebot.driver.dmx import DmxDriver
from moebot.database import CocktailDb, LocalDb, AggregateDb
from moebot.coordinator import Coordinator, MissingIngredients
from moebot.config import Config
import yaml

CONF_FILE = "moebot.yml"

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

DEFAULT_CFG = {
    "driver": {
        "type": "dmx",
        "port": "/dev/ttyUSB0",
        "offset": 1,
        "calibration": [
            50,
            50,
            50,
            50,
            50,
            50,
            50,
            50,
        ],
    },
    "databases": [
        {"type": "local"},
        {"type": "cocktaildb"},
    ],
    "config": {
        "slots": [
            "kahlua",
            "vodka",
            "pineapple rum",
            "whiskey",
            "ginger ale",
            "bloody mary",
            "wine",
            "triple sec",
        ],
    },
}


def main():
    conf_data = DEFAULT_CFG

    try:
        with open(CONF_FILE) as f:
            conf_data = yaml.load(f)
    except (IOError, OSError):
        pass

    config = Config(slots=conf_data.get("config", {}).get("slots", []))

    driver = None
    driver_opts = conf_data.get("driver", {})
    driver_type = driver_opts.pop("type", None)

    if driver_type == "dmx":
        driver = DmxDriver(**driver_opts)
    else:
        print(f"Invalid driver type '{driver_type}'")
        exit(1)

    db = None

    inner_dbs = []
    for db_opts in conf_data.get("databases", []):
        db_type = db_opts.pop("type", None)
        if db_type == "cocktaildb":
            inner_dbs.append(CocktailDb())
        elif db_type == "local":
            inner_dbs.append(LocalDb(config))
        else:
            print(f"Invalid database type '{db_type}'")
            exit(1)

    if len(inner_dbs) == 1:
        db = inner_dbs[0]
    else:
        db = AggregateDb(*inner_dbs)

    coordinator = Coordinator(config)

    try:
        while True:
            search = input("Enter a drink: ")

            search_res = db.search(search)

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
