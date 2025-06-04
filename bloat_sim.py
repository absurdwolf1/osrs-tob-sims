from random import randrange
from math import floor
from statistics import mode
from statistics import stdev
from Bloat import Bloat
from WeaponConstants import *


MIN_DOWN_TICKS = 39
MAX_DOWN_TICKS = 53
BACKUP_THRESHOLD = 35
HUMID_CYCLE_START_TICK = 16
NON_HUMID_CYCLE_START_TICK = 27
BLOAT_SLEEP_TICKS = 32
TEAM_SIZE = 5
DEATH_ANIMATION_SECONDS = 1.8

trials = 10000

SBS_FRZ = True

BLOAT_HP_5_MAN = 2000
BLOAT_DEFENSE = 100
BLOAT_SLASH_DEFENSE = 20
BLOAT_CRUSH_DEFENSE = 40
BLOAT_STANDARD_RANGE_DEFENSE = 800
BLOAT_HEAVY_RANGE_DEFENSE = 800


def main():
    totalTime = 0
    walkTime = 0
    failedBloatCount = 0
    sub40Count = 0
    fastestTime = 1000000000
    times = []
    for x in range(trials):
        timeToKill, walkTime = killBloat()
        if timeToKill < 0:
            failedBloatCount += 1
        else:
            if timeToKill < 41:
                sub40Count += 1
            totalTime += timeToKill
            times.append(timeToKill)
            if fastestTime > timeToKill:
                fastestTime = timeToKill

    if totalTime > 0:

        averageTimeSeconds = totalTime / len(times)

        averageTimeDisplayMinutes = floor(averageTimeSeconds / 60)
        averageTimeDisplaySeconds = round(averageTimeSeconds % 60, 2)
        print("Average Time: ", averageTimeDisplayMinutes, " minutes and ", averageTimeDisplaySeconds, "seconds")
        #print("Walking Time: ", walkTime, " seconds")

        print("Mode: ", round(mode(times), 2), " seconds")
        if trials > 2:
            print("Std Dev:", round(stdev(times), 2), " seconds")

        fastestTimeDisplayMinutes = floor(fastestTime / 60)
        fastestTimeDisplaySeconds = round(fastestTime % 60, 2)
        print("Fastest Time: ", fastestTimeDisplayMinutes, " minutes and ", fastestTimeDisplaySeconds, "seconds")
        print("Failed Bloats: ", failedBloatCount)

        percentSub40 = sub40Count / len(times) * 100
        print("Percent of Bloats 40 seconds and Under: ", round(percentSub40, 2))
    else:
        print("Failed to kill Bloat")
        print("Walking Time: ", walkTime, " seconds")


def killBloat():
    bloat = Bloat(BLOAT_HP_5_MAN, BLOAT_DEFENSE, BLOAT_SLASH_DEFENSE, BLOAT_CRUSH_DEFENSE, BLOAT_STANDARD_RANGE_DEFENSE,
                  BLOAT_HEAVY_RANGE_DEFENSE)

    # find how long bloat is walking for
    walkTimeTicks = getWalkTIme()

    # get player 1's scythe and bgs damage
    bloat.getScytheSalve()
    bloat.getBgsSalve()

    # get player 2's scythe damage
    bloat.getScytheSalve()
    bloat.getScytheSalve()
    bloat.getScythePneck()

    # get player 3's bgs dmg
    backedUpOnce = bloat.getDefense() > BACKUP_THRESHOLD
    if backedUpOnce:
        bloat.getBgsSalve()
    else:
        bloat.getScytheSalve()

    backedUpTwice = bloat.getDefense() > BACKUP_THRESHOLD
    if backedUpTwice:
        bloat.getBgsSalve()
    else:
        bloat.getScytheSalve()

    # start the humid cycle
    # this is how many scythe hits each humider gets before bloat stops walking
    humidScytheHitsWalking = floor((walkTimeTicks - HUMID_CYCLE_START_TICK) / 5)
    humidScytheCoolDown = (walkTimeTicks - HUMID_CYCLE_START_TICK) % 5

    if SBS_FRZ:
        players_on_lunars = TEAM_SIZE - 1
    else:
        players_on_lunars = TEAM_SIZE - 2

    for x in range(humidScytheHitsWalking):
        bloat.setDefense(bloat.getDefense() + 5)  # bloat regens a defense level every tick he is walking
        for y in range(players_on_lunars):
            bloat.getScythePneck()


    # if sbs frz, the non-humid necker starts the same time as the humid neckers
    if SBS_FRZ:
        nonHumidScytheHitsWalking = floor((walkTimeTicks - NON_HUMID_CYCLE_START_TICK) / 5)
    else:
        nonHumidScytheHitsWalking = floor((walkTimeTicks - HUMID_CYCLE_START_TICK) / 5)

    bloat.getScytheSalve()
    bloat.getScytheSalve()
    for x in range(nonHumidScytheHitsWalking - 2):
        bloat.getScythePneck()

    # bloat will stop walking, figure out how many scythe hits each person has before bloat wakes up
    bloat.stopWalking()
    playerTicks = []
    for x in range(TEAM_SIZE):
        playerTicks.append(humidScytheCoolDown)

    if backedUpTwice:
        playerThreeSpec = 0
    elif backedUpOnce:
        playerThreeSpec = 50
    else:
        playerThreeSpec = 100

    playerSpec = [50, 100, playerThreeSpec, 100, 100]

    # 3 players have 2 claw specs, 1 player has 1 claw spec, and 1 player might have 0 or 1 or 2 claw specs
    tickKilled = 0
    playerFiveAttackCount = 0
    for sleepTick in range(BLOAT_SLEEP_TICKS):
        for player in range(TEAM_SIZE):
            tick = playerTicks[player]
            spec = playerSpec[player]

            if player == 4 and spec == 100 and not SBS_FRZ:
                # zcb spec
                bloat.getZcbSalve()
                tick = zcbCoolDown
                spec -= zcbSpecPercent
                playerFiveAttackCount += 1
            else:
                if player == 4 and playerFiveAttackCount == 4 and not SBS_FRZ:
                    # Chally spec after 3 scythe hits
                    bloat.getChallySalve()
                    tick = challyCoolDown
                    spec -= challySpecPercent
                    playerFiveAttackCount += 1
                else:
                    dmg, tick, spec = getPlayerDamage(tick, spec, bloat)
            playerTicks[player] = tick
            playerSpec[player] = spec

            if bloat.isDead():
                tickKilled = sleepTick
                break

        if bloat.isDead():
            break

    if not bloat.isDead():
        killTime = -1
    else:
        killTime = walkTimeTicks * 0.6 + tickKilled * 0.6 + DEATH_ANIMATION_SECONDS
    return killTime, walkTimeTicks * 0.6


def getPlayerDamage(tick, spec, bloat):
    dmg = 0
    if tick == 0:
        if spec >= clawSpecPercent:
            bloat.getClawSalve()
            spec -= clawSpecPercent
            tick = clawCoolDown
        else:
            bloat.getScytheSalve()
            tick = scytheCoolDown
    else:
        tick -= 1

    return dmg, tick, spec


def getWalkTIme():
    return randrange(MIN_DOWN_TICKS, MAX_DOWN_TICKS)


if __name__ == "__main__":
    main()
