from moebot.drink import Pour


class MissingIngredients(Exception):
    def __init__(self, ingredients):
        super().__init__("Missing ingredients: " + ','.join(ingredients))

        self.ingredients = ingredients


class Coordinator:
    def __init__(self, config):
        self.config = config

    def make_drink(self, driver, drink, ignore_missing=False):
        for step in drink.steps:
            # TODO don't ignore all the other steps
            if isinstance(step, Pour):

                if not ignore_missing:
                    missing = []
                    # Check if config can support all things
                    for ingredient, _ in step.ingredients:
                        slot = self.config.slot_for(ingredient)
                        if slot is None:
                            missing.append(ingredient)

                    if missing:
                        raise MissingIngredients(missing)

                # Pour the smallest ingredients first for better mixage
                pours = sorted(step.ingredients, key=lambda ing: ing[1])

                for ingredient, amount in pours:
                    slot = self.config.slot_for(ingredient)

                    if slot is not None:
                        print(f"Dispensing {amount:0.2f} {ingredient} via drink slot {slot}")
                        driver.dispense(slot, amount)
