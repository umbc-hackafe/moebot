class Config:
    def __init__(self, slots=None):
        self.slots = slots or [None] * 8

    def slots(self):
        return self.slots

    def slot_for(self, ingredient):
        for index, slot in enumerate(self.slots):
            if slot.lower() in ingredient.lower() or ingredient.lower() in slot.lower():
                return index

        return None
