from dataclasses import dataclass
import WeaponConstants


@dataclass
class GearSet:
    maxHit: int
    attackRoll: int
    coolDown: int


scytheOath = GearSet(WeaponConstants.scytheOathMax,
                     WeaponConstants.scytheOathAttackRoll,
                     WeaponConstants.scytheCoolDown)

scytheOathSalve = GearSet(WeaponConstants.scytheMaxSalve,
                          WeaponConstants.scytheSalveAttackRoll,
                          WeaponConstants.scytheCoolDown)

scytheOathPneck = GearSet(WeaponConstants.scytheMaxPneck,
                          WeaponConstants.scythePneckAttackRoll,
                          WeaponConstants.scytheCoolDown)

tbowMasori = GearSet(WeaponConstants.tbowMaxMasori,
                     WeaponConstants.tbowAttackRollMasori,
                     WeaponConstants.tbowCoolDown)

tbowVoid = GearSet(WeaponConstants.tbowMaxVoid,
                   WeaponConstants.tbowAttackRollVoid,
                   WeaponConstants.tbowCoolDown)

maxRange = GearSet(WeaponConstants.tbowMaxVoidAng,
                   WeaponConstants.tbowAttackRollVoid,
                   WeaponConstants.tbowCoolDown)

tbowMasoriAng = GearSet(WeaponConstants.tbowMaxMasoriAng,
                        WeaponConstants.tbowAttackRollVoid,
                        WeaponConstants.tbowCoolDown)

tbowTorva = GearSet(WeaponConstants.tbowMaxTorva,
                    WeaponConstants.tbowAttackRollTorva,
                    WeaponConstants.tbowCoolDown)

sangVirtus = GearSet(WeaponConstants.sangMaxVirtus,
                     WeaponConstants.sangAttackRollVirtus,
                     WeaponConstants.sangCoolDown)

sangTorva = GearSet(WeaponConstants.sangMaxTorva,
                    WeaponConstants.sangAttackRollTorva,
                    WeaponConstants.sangCoolDown)

shadowAnc = GearSet(WeaponConstants.shadowMax,
                    WeaponConstants.shadowAttackRoll,
                    WeaponConstants.shadowCoolDown)
