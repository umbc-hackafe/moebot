class Step:
    def do(self, controllers):
        pass

    def __str__(self):
        return "Do a thing"


class Ice(Step):
    def __str__(self):
        return "Add ice"


class Rim(Step):
    def __init__(self, target="salt"):
        self.target = target

    def do(self, controllers):
        # Control the arm here
        pass

    def __str__(self):
        return f"Rim glass with f{self.target}"


class Garnish(Step):
    def __init__(self, kind):
        self.kind = kind

    def __str__(self):
        return f"Garnish with {self.kind}"


class Wedge(Step):
    def __init__(self, kind):
        self.kind = kind

    def __str__(self):
        return f"Add a {self.kind} wedge"


class Pour(Step):
    def __init__(self, *ingredients):
        self.ingredients = ingredients

    def __str__(self):
        ing_descs = ", ".join((f"{i[1]:.1f} {i[0]}" for i in self.ingredients))
        return "Pour " + ing_descs


class Drink:
    def __init__(self, name, *steps):
        self.name = name
        self.steps = steps

    def __str__(self):
        return f"{self.name}: " + ", ".join((str(s) for s in self.steps))
