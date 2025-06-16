import GearSets
from Player import Player
from PrintTobStats import *
from Nylo import Nylo
import numpy as np
import WeaponConstants

trials = 10000

NYLO_DEF = 50
NYLO_SLASH_DEF = 0
NYLO_CRUSH_DEF = 0
NYLO_STANDARD_RANGE_DEF = 0
NYLO_HEAVY_RANGE_DEF = 0
DEATH_ANIMATION_TICKS = 4
PHASE_LENGTH_TICKS = 10
BOSS_DROP_TIME_TICKS = 3


def main():
    times = np.empty(trials)
    backThreshold = 20
    bpFillThreshold = 0.7
    for x in range(trials):
        players = createPlayers()
        times[x] = killNylo(players, backThreshold, bpFillThreshold)

    times = sorted(times)
    printStats(times)
    plotTimes(times, "Nylo Boss", 6)


def killNylo(players, backThreshold, bpFillThreshold):
    TEAM_SIZE = len(players)
    if TEAM_SIZE == 5:
        NYLO_HP = 2500
    elif TEAM_SIZE == 4:
        NYLO_HP = 2187
    else:
        NYLO_HP = 1875

    nylo = Nylo(NYLO_HP, NYLO_DEF, NYLO_SLASH_DEF, NYLO_CRUSH_DEF, NYLO_STANDARD_RANGE_DEF, NYLO_HEAVY_RANGE_DEF)
    #nylo.forceGodBoss()

    # find the player with the bgs
    bgsPlayer = players[TEAM_SIZE - 1]
    for player in players:
        if "bgs" in player.specWeapons:
            bgsPlayer = player

        # the player can't attack the same tick the boss spawns
        # start the room at tick 1 to take this into account
    roomTimeTicks = 1
    while nylo.getHp() > 0:
        roomTimeTicks += 1

        # change the phase every 10 ticks
        if roomTimeTicks % PHASE_LENGTH_TICKS == 0:
            nylo.changePhase()
            # a player cannot attack the same tick the boss changes phases
            # decrement all the cool downs by 1 then continue
            for player in players:
                player.decreaseWeaponCoolDown()
            continue

        for player in players:
            if player.weaponCoolDown == 0:
                if nylo.phase == "melee":
                    # bgs the boss if the bgs player has enough spec and is above the backup threshold
                    if "bgs" in player.specWeapons \
                            and player.spec >= WeaponConstants.bgsSpecPercent \
                            and nylo.defense > backThreshold:
                        player.bgsSpec(nylo)
                    # chally the boss if the bgs player has already bgs'd once
                    elif bgsPlayer.spec < 100 \
                            and "chally" in player.specWeapons \
                            and player.spec >= WeaponConstants.challySpecPercent:
                        player.challySpec(nylo)
                        # remove chally from the player's spec weapons so they don't chally again
                        player.specWeapons.remove("chally")
                    else:
                        player.meleeAttack(nylo)
                elif nylo.phase == "range":
                    # if the player has a zcb spec ready
                    if player.spec >= WeaponConstants.zcbSpecPercent and "zcb" in player.specWeapons:
                        player.zcbSpec(nylo)
                    # check to see if the player can blowpipe fill
                    # (attacking 6 or 7 ticks after the previous phase change)
                    # and the nylo boss is above a certain hp threshold
                    elif nylo.hp > bpFillThreshold * NYLO_HP \
                            and (roomTimeTicks % PHASE_LENGTH_TICKS == 6
                                 or roomTimeTicks % PHASE_LENGTH_TICKS == 7):
                        player.blowpipe(nylo)
                    else:
                        player.rangeAttack(nylo)
                elif nylo.phase == "mage":
                    player.mageAttack(nylo)
            else:
                player.decreaseWeaponCoolDown()

    return roomTimeTicks + DEATH_ANIMATION_TICKS + BOSS_DROP_TIME_TICKS


def createPlayers():
    players = []

    # NORTH MAGE
    player1 = Player()
    player1.setSpec(105, ["chally", "zcb"])
    player1.setMeleeGear(GearSets.scytheOath)
    player1.setRangeGear(GearSets.tbowMasori)
    # player1.setMageGear(GearSets.shadowAnc)
    player1.setMageGear(GearSets.sangVirtus)
    players.append(player1)

    # MAGE DPS
    player2 = Player()
    player2.setSpec(105, ["chally", "zcb"])
    player2.setMeleeGear(GearSets.scytheOath)
    player2.setRangeGear(GearSets.tbowMasori)
    player2.setMageGear(GearSets.sangVirtus)
    players.append(player2)

    # RANGE
    player3 = Player()
    player3.setSpec(105, ["chally", "zcb"])
    player3.setMeleeGear(GearSets.scytheOath)
    player3.setRangeGear(GearSets.tbowVoid)
    player3.setMageGear(GearSets.sangTorva)
    players.append(player3)

    # MELEE 1
    player4 = Player()
    player4.setSpec(105, ["chally", "zcb"])
    player4.setMeleeGear(GearSets.scytheOath)
    player4.setRangeGear(GearSets.tbowTorva)
    player4.setMageGear(GearSets.sangTorva)
    players.append(player4)

    # MELEE 2
    player5 = Player()
    player5.setSpec(125, ["bgs", "zcb"])
    player5.setMeleeGear(GearSets.scytheOath)
    player5.setRangeGear(GearSets.tbowTorva)
    player5.setMageGear(GearSets.sangTorva)
    players.append(player5)

    return players


if __name__ == "__main__":
    main()
