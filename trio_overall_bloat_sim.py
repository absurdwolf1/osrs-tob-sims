import WeaponConstants
from Bloat import Bloat
from PrintTobStats import *


BACKUP_THRESHOLD = 35
BLOAT_SLEEP_TICKS = 32
TEAM_SIZE = 3
DEATH_ANIMATION_SECONDS = 1.8
MIN_WALK_TICK_TO_SURVIVE = 44

trials = 1000

BLOAT_HP = 1500
BLOAT_DEFENSE = 100
BLOAT_SLASH_DEFENSE = 20
BLOAT_CRUSH_DEFENSE = 40
BLOAT_STANDARD_RANGE_DEFENSE = 800
BLOAT_HEAVY_RANGE_DEFENSE = 800


def main():
    times = []
    bloatFailsFromDamage = 0
    bloatFailsFromLongWalk = 0
    for x in range(trials):
        time = killBloat()
        if time == -1:
            bloatFailsFromDamage += 1
        elif time == -2:
            bloatFailsFromLongWalk += 1
        else:
            times.append(time)

    bloatFails = bloatFailsFromDamage + bloatFailsFromLongWalk
    bloatsKilled = trials - bloatFails
    print("Percent of Bloats killed: ", bloatsKilled / trials * 100, "%")
    print("Percent of Bloats not killed: ", bloatFails / trials * 100, "%")
    print("Percent of Bloats not killed because of bad damage: ", bloatFailsFromDamage / trials * 100, "%")
    print("Percent of Bloats not killed running out of necks: ", bloatFailsFromLongWalk / trials * 100, "%")

    if bloatsKilled > 0:
        times = sorted(times)
        printStats(times)


def killBloat():
    bloat = Bloat(BLOAT_HP, BLOAT_DEFENSE, BLOAT_SLASH_DEFENSE, BLOAT_CRUSH_DEFENSE, BLOAT_STANDARD_RANGE_DEFENSE,
                  BLOAT_HEAVY_RANGE_DEFENSE)
    # player 1 = mage
    # player 2 = range
    # player 3 = mdps

    # find out if the team has enough necks to live
    if bloat.walkTime > MIN_WALK_TICK_TO_SURVIVE:
        return -2

    # TODO pre-allocate array based on TEAM_SIZE
    # TODO pre-bgs scythe salve hits vs post-bgs scythe salve hits
    salveScytheHits = [1, 0, 2]
    neckingStartTick = [28, 23, 18]  # TODO add one if walking the opposite direction
    playerSpec = [125, 100, 100]
    bgsSpecs = [1, 0, 2]
    zcbSpecs = [1, 0, 0]
    clawSpecs = [0, 2, 2]

    # Apply bgs specs
    for player in range(TEAM_SIZE):
        numberOfBgsSpecs = bgsSpecs[player]
        for x in range(numberOfBgsSpecs):
            if bloat.defense > BACKUP_THRESHOLD:
                bloat.getBgsSalve()
                playerSpec[player] -= 50

    # Apply salve scythe hits
    for salveScytheHit in salveScytheHits:
        for x in range(salveScytheHit):
            bloat.getScytheSalve()

    # start necking
    roomTimeTicks = 0
    playerTicks = [0, 0, 0]  # TODO pre-allocate based on team size
    # find out how long bloat will be walking + sleeping, then add 5 to account for tick eating the stomp
    bloatAliveTime = bloat.getWalkTIme() + BLOAT_SLEEP_TICKS + 5
    while bloat.getHp() > 0:
        roomTimeTicks += 1

        # figure out if bloat has gone to sleep
        if bloat.isWalking and roomTimeTicks >= bloat.getWalkTIme():
            bloat.stopWalking()

        for player in range(TEAM_SIZE):
            # find out if the player is necking or not yet
            startNeckingTick = neckingStartTick[player]
            if startNeckingTick == 0:
                # if they are necking, scythe bloat with a pneck on if bloat is still walking
                # otherwise scythe with a salve on
                tick = playerTicks[player]
                if tick == 0:
                    if bloat.isWalking:
                        bloat.getScythePneck()
                        playerTicks[player] = WeaponConstants.scytheCoolDown
                    else:
                        # players can spec once bloat is sleeping
                        # if no spec is available, just scythe bloat
                        spec = playerSpec[player]
                        zcbSpec = zcbSpecs[player]
                        clawSpec = clawSpecs[player]
                        if spec >= 75 and zcbSpec > 0:
                            bloat.getZcbSalve()
                            playerSpec[player] -= WeaponConstants.zcbSpecPercent
                            playerTicks[player] = WeaponConstants.zcbCoolDown
                        elif spec >= 50 and clawSpec > 0:
                            bloat.getClawSalve()
                            playerSpec[player] -= WeaponConstants.clawSpecPercent
                            playerTicks[player] = WeaponConstants.clawCoolDown
                        else:
                            bloat.getScytheSalve()
                            playerTicks[player] = WeaponConstants.scytheCoolDown
                else:
                    playerTicks[player] -= 1
            else:
                neckingStartTick[player] -= 1

        if roomTimeTicks > bloatAliveTime:
            # you have failed to kill bloat
            break

    # if bloat is dead, return room time, otherwise return -1 to signal bloat was not killed
    if not bloat.isDead():
        return -1
    else:
        return roomTimeTicks + DEATH_ANIMATION_SECONDS


if __name__ == "__main__":
    main()
