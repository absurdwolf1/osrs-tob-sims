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

    def setMeleeGear(self, gearSet):
        self.meleeMaxHit = gearSet.maxHit
        self.meleeAttackRoll = gearSet.attackRoll
        self.meleeCoolDown = gearSet.coolDown

    def setRangeGear(self, gearSet):
        self.rangeMaxHit = gearSet.maxHit
        self.rangeAttackRoll = gearSet.attackRoll
        self.rangeCoolDown = gearSet.coolDown

    def setMageGear(self, gearSet):
        self.mageMaxHit = gearSet.maxHit
        self.mageAttackRoll = gearSet.attackRoll
        self.mageCoolDown = gearSet.coolDown

    def meleeAttack(self, monster):
        monster.doScytheAttack(self.meleeMaxHit, self.meleeAttackRoll)
        self.weaponCoolDown = self.meleeCoolDown

    def rangeAttack(self, monster):
        monster.doAttack(self.rangeMaxHit, self.rangeAttackRoll, monster.standardRangeDefense)
        self.weaponCoolDown = self.rangeCoolDown

    def mageAttack(self, monster):
        monster.doAttack(self.mageMaxHit, self.mageAttackRoll, 0)  # TODO add mage defense
        self.weaponCoolDown = self.mageCoolDown

    def maulSpec(self, monster, horned):
        monster.getMaulHit()
        self.weaponCoolDown = WeaponConstants.maulCoolDown
        self.spec -= WeaponConstants.maulCoolDown

    def bgsSpec(self, monster):
        monster.getBgs()
        self.weaponCoolDown = WeaponConstants.bgsCoolDown
        self.spec -= WeaponConstants.bgsSpecPercent

    def challySpec(self, monster):
        monster.getChally()
        self.weaponCoolDown = WeaponConstants.challyCoolDown
        self.spec -= WeaponConstants.challySpecPercent

    def zcbSpec(self, monster):
        monster.getZcb()
        self.weaponCoolDown = WeaponConstants.zcbCoolDown
        self.spec -= WeaponConstants.zcbSpecPercent

    def blowpipe(self, monster):
        # TODO bp rolls against light range def
        # figure out what range gear the player is using
        if self.rangeMaxHit == WeaponConstants.tbowMaxVoid:
            bpMax = WeaponConstants.blowpipeMaxVoid
        elif self.rangeMaxHit == WeaponConstants.tbowMaxMasori:
            bpMax = WeaponConstants.blowpipeMaxMasori
        else:
            bpMax = WeaponConstants.blowpipeMaxTorva

        monster.doAttack(bpMax,
                         WeaponConstants.blowpipeAttackRoll,
                         monster.standardRangeDefense)

        self.weaponCoolDown = WeaponConstants.blowpipeCoolDown

    def decreaseWeaponCoolDown(self):
        self.weaponCoolDown -= 1
