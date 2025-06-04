from Monster import Monster


class Sote(Monster):
    def __init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense):
        Monster.__init__(self, hp, defense, slashDefense, crushDefense, standardRangeDefense, heavyRangeDefense)

    def setDefense(self, d):
        if d < 100:
            d = 100
        self.defense = d
