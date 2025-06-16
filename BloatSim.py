import WeaponConstants
from Bloat import Bloat
import GearSets
from Player import Player
from PrintTobStats import *


BACKUP_THRESHOLD = 25
BLOAT_SLEEP_TICKS = 32
TEAM_SIZE = 5
DEATH_ANIMATION_TICKS = 3
CHALLY_THRESHOLD_PERCENT = 0.10

trials = 10000

BLOAT_HP_5_MAN = 2000
BLOAT_DEFENSE = 100
BLOAT_SLASH_DEFENSE = 20
BLOAT_CRUSH_DEFENSE = 40
BLOAT_STANDARD_RANGE_DEFENSE = 800
BLOAT_HEAVY_RANGE_DEFENSE = 800


def main():
    times = []
    for x in range(trials):
        players = createPlayers()
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)

    times = sorted(times)
    printStats(times)
    plotTimes(times, "Bloat", 6)


def killBloat(players, walkingTime, backupThreshold):
    bloat = Bloat(BLOAT_HP_5_MAN, BLOAT_DEFENSE, BLOAT_SLASH_DEFENSE, BLOAT_CRUSH_DEFENSE, BLOAT_STANDARD_RANGE_DEFENSE,
                  BLOAT_HEAVY_RANGE_DEFENSE)

    if walkingTime > 0:
        bloat.setWalkTime(walkingTime)

    if backupThreshold < 0:
        backupThreshold = BACKUP_THRESHOLD

    # north south range mel 1 mel 2
    neckingStartTick = [27, 9, 16, 2, 9]
    scytheSalveHits = [2, 2, 2, 1, 0]

    # start necking
    roomTimeTicks = 1
    while bloat.getHp() > 0:
        roomTimeTicks += 1

        if roomTimeTicks == bloat.getWalkTIme():
            bloat.stopWalking()
            for player in players:
                player.setMeleeGear(GearSets.scytheOathSalve)

        for x in range(len(players)):
            player = players[x]
            playerStartTick = neckingStartTick[x]

            # special case where player 4 is running around the room between tick 8 and 15
            if x == 3 and 9 <= roomTimeTicks <= 15:
                player.decreaseWeaponCoolDown()
                continue

            if player.weaponCoolDown == 0 and roomTimeTicks >= playerStartTick:
                # bgs the boss
                if "bgs" in player.specWeapons \
                        and player.spec >= WeaponConstants.bgsSpecPercent \
                        and bloat.getDefense() > backupThreshold:
                    player.bgsSpecSalve(bloat)

                elif "zcb" in player.specWeapons \
                        and player.spec >= WeaponConstants.zcbSpecPercent \
                        and not bloat.isWalking:
                    player.zcbSpecSalve(bloat)

                # handle claw specs
                elif "claw" in player.specWeapons \
                        and player.spec >= WeaponConstants.clawSpecPercent \
                        and not bloat.isWalking:
                    player.clawSpecSalve(bloat)

                # scythe the boss
                elif "chally" in player.specWeapons \
                        and player.spec >= WeaponConstants.challySpecPercent \
                        and not bloat.isWalking \
                        and bloat.hp <= CHALLY_THRESHOLD_PERCENT * BLOAT_HP_5_MAN:
                    player.challySpecSalve(bloat)
                else:
                    salveOrPneckCount = scytheSalveHits[x]
                    if salveOrPneckCount > 0:
                        player.meleeAttack(bloat)
                        scytheSalveHits[x] = salveOrPneckCount - 1
                        if salveOrPneckCount - 1 == 0:
                            player.setMeleeGear(GearSets.scytheOathPneck)
                    else:
                        player.meleeAttack(bloat)
            else:
                player.decreaseWeaponCoolDown()

        if roomTimeTicks > bloat.getWalkTIme() + BLOAT_SLEEP_TICKS:
            # you have failed to kill bloat
            break

    # if bloat is dead, return room time, otherwise return -1 to signal bloat was not killed
    if not bloat.isDead():
        return -1
    else:
        return roomTimeTicks + DEATH_ANIMATION_TICKS


def createPlayers():
    players = []

    # NORTH MAGE
    player1 = Player()
    player1.setSpec(130, ["claw", "claw", "chally"])
    player1.setMeleeGear(GearSets.scytheOathSalve)
    player1.setRangeGear(GearSets.tbowMasori)
    players.append(player1)

    # MAGE DPS
    player2 = Player()
    player2.setSpec(125, ["Zcb", "claw"])
    player2.setMeleeGear(GearSets.scytheOathSalve)
    player2.setRangeGear(GearSets.tbowMasori)
    players.append(player2)

    # RANGE
    player3 = Player()
    player3.setSpec(125, ["claw", "claw"])
    player3.setMeleeGear(GearSets.scytheOathSalve)
    player3.setRangeGear(GearSets.tbowVoid)
    players.append(player3)

    # MELEE 1
    player4 = Player()
    player4.setSpec(125, ["bgs", "claw"])
    player4.setMeleeGear(GearSets.scytheOathSalve)
    player4.setRangeGear(GearSets.tbowTorva)
    players.append(player4)

    # MELEE 2
    player5 = Player()
    player5.setSpec(125, ["bgs", "claw"])
    player5.setMeleeGear(GearSets.scytheOathPneck)
    player5.setRangeGear(GearSets.tbowTorva)
    players.append(player5)

    return players


if __name__ == "__main__":
    main()
