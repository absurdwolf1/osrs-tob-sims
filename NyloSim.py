from Player import Player
from PrintTobStats import *
from Nylo import Nylo
import numpy as np
import WeaponConstants

NYLO_HP = 2500
NYLO_DEF = 50
NYLO_SLASH_DEF = 0
NYLO_CRUSH_DEF = 0
NYLO_STANDARD_RANGE_DEF = 0
NYLO_HEAVY_RANGE_DEF = 0
TEAM_SIZE = 5
DEATH_ANIMATION_TICKS = 4

bgs = True
bgsHit = -1
BACKUP_THRESHOLD = 15

trials = 10000

PHASE_LENGTH_TICKS = 10
BOSS_DROP_TIME = 3


def main():
    times = np.empty(trials)
    for x in range(trials):
        times[x] = killNylo()

    times = sorted(times)
    printStats(times)

    plotTimes(times, "Nylo Boss", 6)


def killNylo():
    nylo = Nylo(NYLO_HP, NYLO_DEF, NYLO_SLASH_DEF, NYLO_CRUSH_DEF, NYLO_STANDARD_RANGE_DEF, NYLO_HEAVY_RANGE_DEF)
    nylo.forceGodBoss()

    players = createPlayers()

    # hard-code 1st phase to deal with scythe -> chally and bgs specs
    # everyone does 1 scythe into a chally spec, the bgs player does a bgs and either backs up or scythes
    for player in range(TEAM_SIZE - 1):
        players[player].meleeAttack(nylo)

    # TODO better way to do this
    bgsPlayer = players[TEAM_SIZE - 1]
    nylo.getBgs()
    bgsPlayer.setSpec(75, bgsPlayer.specWeapons)

    for player in range(TEAM_SIZE - 1):
        nylo.getChally()

    backup = nylo.getDefense() > BACKUP_THRESHOLD
    if backup:
        nylo.getBgs()
        bgsPlayer.setSpec(0, bgsPlayer.specWeapons)
        bgsPlayer.weaponCoolDown = 4
    else:
        bgsPlayer.meleeAttack(nylo)
        bgsPlayer.weaponCoolDown = 3

    # 1st phase is 10 ticks long, plus 3 ticks it takes for the boss to drop from the ceiling
    roomTimeTicks = 13

    while nylo.getHp() > 0:
        # change the phase every 10 ticks
        if (roomTimeTicks - BOSS_DROP_TIME) % PHASE_LENGTH_TICKS == 0:
            nylo.changePhase()

        roomTimeTicks += 1

        for player in players:
            if player.weaponCoolDown == 0:
                if nylo.phase == "melee":
                    player.meleeAttack(nylo)
                elif nylo.phase == "range":
                    if player.spec >= WeaponConstants.zcbSpecPercent and "zcb" in player.specWeapons:
                        player.zcbSpec(nylo)
                    else:
                        player.rangeAttack(nylo)
                elif nylo.phase == "mage":
                    player.mageAttack(nylo)
            else:
                player.decreaseWeaponCoolDown()

    return roomTimeTicks + DEATH_ANIMATION_TICKS


# TODO better way to create this
# maybe have "set" classes aka oath, void, virtus, etc
def createPlayers():
    players = []

    # NORTH MAGE
    # melee: oath scythe
    # range: tbow masori
    # mage: sang virtus
    player1 = Player()
    player1.setSpec(75, "zcb")
    player1.setMeleeGear(WeaponConstants.scytheOathMax,
                         WeaponConstants.scytheOathAttackRoll,
                         WeaponConstants.scytheCoolDown)
    player1.setRangeGear(WeaponConstants.tbowMaxMasori,
                         WeaponConstants.tbowAttackRollMasori,
                         WeaponConstants.tbowCoolDown)
    player1.setMageGear(WeaponConstants.sangMaxVirtus,
                        WeaponConstants.sangAttackRollVirtus,
                        WeaponConstants.sangCoolDown)
    # player1.setMageGear(WeaponConstants.shadowMax,
    #                     WeaponConstants.shadowAttackRoll,
    #                     WeaponConstants.shadowCoolDown)
    players.append(player1)

    # MAGE DPS
    # melee: oath scythe
    # range: tbow torva
    # mage: sang virtus
    player2 = Player()
    player2.setSpec(75, "zcb")
    player2.setMeleeGear(WeaponConstants.scytheOathMax,
                         WeaponConstants.scytheOathAttackRoll,
                         WeaponConstants.scytheCoolDown)
    player2.setRangeGear(WeaponConstants.tbowMaxTorva,
                         WeaponConstants.tbowAttackRollTorva,
                         WeaponConstants.tbowCoolDown)
    player2.setMageGear(WeaponConstants.sangMaxVirtus,
                        WeaponConstants.sangAttackRollVirtus,
                        WeaponConstants.sangCoolDown)
    players.append(player2)

    # RANGE
    # melee: oath scythe
    # range: tbow void
    # mage: sang torva
    player3 = Player()
    player3.setSpec(75, "zcb")
    player3.setMeleeGear(WeaponConstants.scytheOathMax,
                         WeaponConstants.scytheOathAttackRoll,
                         WeaponConstants.scytheCoolDown)
    player3.setRangeGear(WeaponConstants.tbowMaxVoid,
                         WeaponConstants.tbowAttackRollVoid,
                         WeaponConstants.tbowCoolDown)
    player3.setMageGear(WeaponConstants.sangMaxTorva,
                        WeaponConstants.sangAttackRollTorva,
                        WeaponConstants.sangCoolDown)
    players.append(player3)

    # MELEE 1
    # melee: oath scythe
    # range: tbow torva
    # mage: sang torva
    player4 = Player()
    player4.setSpec(75, "zcb")
    player4.setMeleeGear(WeaponConstants.scytheOathMax,
                         WeaponConstants.scytheOathAttackRoll,
                         WeaponConstants.scytheCoolDown)
    player4.setRangeGear(WeaponConstants.tbowMaxTorva,
                         WeaponConstants.tbowAttackRollTorva,
                         WeaponConstants.tbowCoolDown)
    player4.setMageGear(WeaponConstants.sangMaxTorva,
                        WeaponConstants.sangAttackRollTorva,
                        WeaponConstants.sangCoolDown)
    players.append(player4)

    # MELEE 2
    # melee: oath scythe
    # range: tbow torva
    # mage: sang torva
    player5 = Player()
    player5.setSpec(125, "zcb")
    player5.setMeleeGear(WeaponConstants.scytheOathMax,
                         WeaponConstants.scytheOathAttackRoll,
                         WeaponConstants.scytheCoolDown)
    player5.setRangeGear(WeaponConstants.tbowMaxTorva,
                         WeaponConstants.tbowAttackRollTorva,
                         WeaponConstants.tbowCoolDown)
    player5.setMageGear(WeaponConstants.sangMaxTorva,
                        WeaponConstants.sangAttackRollTorva,
                        WeaponConstants.sangCoolDown)
    players.append(player5)

    return players


if __name__ == "__main__":
    main()
