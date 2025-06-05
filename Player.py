import WeaponConstants
from Monster import Monster as Monster


class Player:
    def __init__(self):
        self.spec = 100
        self.specWeapons = []
        self.weaponCoolDown = 0

        self.meleeMaxHit = 0
        self.meleeAttackRoll = 0
        self.meleeCoolDown = 5

        self.rangeMaxHit = 0
        self.rangeAttackRoll = 0
        self.rangeCoolDown = 5

        self.mageMaxHit = 0
        self.mageAttackRoll = 0
        self.mageCoolDown = 5

    def setSpec(self, spec, specWeapons):
        self.specWeapons = specWeapons
        self.spec = spec

    def setMeleeGear(self, maxHit, attackRoll, coolDown):
        self.meleeMaxHit = maxHit
        self.meleeAttackRoll = attackRoll
        self.meleeCoolDown = coolDown

    def setRangeGear(self, maxHit, attackRoll, coolDown):
        self.rangeMaxHit = maxHit
        self.rangeAttackRoll = attackRoll
        self.rangeCoolDown = coolDown

    def setMageGear(self, maxHit, attackRoll, coolDown):
        self.mageMaxHit = maxHit
        self.mageAttackRoll = attackRoll
        self.mageCoolDown = coolDown

    def meleeAttack(self, monster):
        monster.doScytheAttack(self.meleeMaxHit, self.meleeAttackRoll)
        self.weaponCoolDown = self.meleeCoolDown

    def rangeAttack(self, monster):
        monster.doAttack(self.rangeMaxHit, self.rangeAttackRoll, monster.standardRangeDefense)
        self.weaponCoolDown = self.rangeCoolDown

    def mageAttack(self, monster):
        monster.doAttack(self.mageMaxHit, self.mageAttackRoll, 0)  # TODO add mage defense
        self.weaponCoolDown = self.mageCoolDown

    def zcbSpec(self, monster):
        monster.getZcb()
        self.weaponCoolDown = WeaponConstants.zcbCoolDown
        self.spec -= WeaponConstants.zcbSpecPercent

    def decreaseWeaponCoolDown(self):
        self.weaponCoolDown -= 1
