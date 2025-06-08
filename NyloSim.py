import GearSets
from Player import Player
from PrintTobStats import *
from Nylo import Nylo
import numpy as np
import WeaponConstants

TEAM_SIZE = 5
BACKUP_THRESHOLD = 15
BP_FILL_THRESHOLD = 0.3
trials = 10000

if TEAM_SIZE == 5:
    NYLO_HP = 2500
elif TEAM_SIZE == 4:
    NYLO_HP = 2187
else:
    NYLO_HP = 1875

NYLO_DEF = 50
NYLO_SLASH_DEF = 0
NYLO_CRUSH_DEF = 0
NYLO_STANDARD_RANGE_DEF = 0
NYLO_HEAVY_RANGE_DEF = 0
DEATH_ANIMATION_TICKS = 4

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
    #nylo.forceGodBoss()

    players = createPlayers()

    # find the player with the bgs
    bgsPlayer = players[TEAM_SIZE - 1]
    for player in players:
        if "bgs" in player.specWeapons:
            bgsPlayer = player

    roomTimeTicks = 0
    while nylo.getHp() > 0:
        roomTimeTicks += 1

        if roomTimeTicks == 1:
            continue

        # change the phase every 10 ticks
        if roomTimeTicks % PHASE_LENGTH_TICKS == 0:
            nylo.changePhase()

        for player in players:
            if player.weaponCoolDown == 0:
                if nylo.phase == "melee":
                    # bgs the boss if the bgs player has enough spec and is above the backup threshold
                    if "bgs" in player.specWeapons \
                            and player.spec >= WeaponConstants.bgsSpecPercent \
                            and nylo.defense > BACKUP_THRESHOLD:
                        player.bgsSpec(nylo)
                    # chally the boss if the bgs player has already bgs'd once
                    elif bgsPlayer.spec < 100 \
                            and "chally" in player.specWeapons \
                            and player.spec >= WeaponConstants.challySpecPercent:
                        player.challySpec(nylo)
                        player.specWeapons.remove("chally")
                    else:
                        player.meleeAttack(nylo)
                elif nylo.phase == "range":
                    if player.spec >= WeaponConstants.zcbSpecPercent and "zcb" in player.specWeapons:
                        player.zcbSpec(nylo)
                    elif nylo.hp > BP_FILL_THRESHOLD * NYLO_HP \
                            and (roomTimeTicks % PHASE_LENGTH_TICKS == 6
                                 or roomTimeTicks % PHASE_LENGTH_TICKS == 7):
                        player.blowpipe(nylo)
                    else:
                        player.rangeAttack(nylo)
                elif nylo.phase == "mage":
                    player.mageAttack(nylo)
            else:
                player.decreaseWeaponCoolDown()

    return roomTimeTicks + DEATH_ANIMATION_TICKS + BOSS_DROP_TIME


def createPlayers():
    players = []

    # NORTH MAGE
    # melee: oath scythe
    # range: tbow masori
    # mage: sang virtus
    player1 = Player()
    player1.setSpec(105, ["chally", "zcb"])
    player1.setMeleeGear(GearSets.scytheOath)
    player1.setRangeGear(GearSets.tbowMasori)
    # player1.setMageGear(GearSets.shadowAnc)
    player1.setMageGear(GearSets.sangVirtus)
    players.append(player1)

    # MAGE DPS
    # melee: oath scythe
    # range: tbow torva
    # mage: sang virtus
    player2 = Player()
    player2.setSpec(105, ["chally", "zcb"])
    player2.setMeleeGear(GearSets.scytheOath)
    player2.setRangeGear(GearSets.tbowTorva)
    player2.setMageGear(GearSets.sangVirtus)
    players.append(player2)

    # RANGE
    # melee: oath scythe
    # range: tbow void
    # mage: sang torva
    player3 = Player()
    player3.setSpec(105, ["chally", "zcb"])
    player3.setMeleeGear(GearSets.scytheOath)
    player3.setRangeGear(GearSets.tbowVoid)
    player3.setMageGear(GearSets.sangTorva)
    players.append(player3)

    # MELEE 1
    # melee: oath scythe
    # range: tbow torva
    # mage: sang torva
    player4 = Player()
    player4.setSpec(105, ["chally", "zcb"])
    player4.setMeleeGear(GearSets.scytheOath)
    player4.setRangeGear(GearSets.tbowTorva)
    player4.setMageGear(GearSets.sangTorva)
    players.append(player4)

    # MELEE 2
    # melee: oath scythe
    # range: tbow torva
    # mage: sang torva
    player5 = Player()
    player5.setSpec(125, ["bgs", "zcb"])
    player5.setMeleeGear(GearSets.scytheOath)
    player5.setRangeGear(GearSets.tbowTorva)
    player5.setMageGear(GearSets.sangTorva)
    players.append(player5)

    return players


if __name__ == "__main__":
    main()
