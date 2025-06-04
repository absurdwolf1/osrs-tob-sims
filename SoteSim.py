from Sote import Sote
from PrintTobStats import *
import numpy as np
import WeaponConstants
from random import randrange


SOTE_HP = 4000
SOTE_DEF = 200
SOTE_SLASH_DEF = 70
SOTE_CRUSH_DEF = 70
SOTE_STANDARD_RANGE_DEF = 150
SOTE_HEAVY_RANGE_DEF = 150
SOTE_MAX_HIT = 50
TEAM_SIZE = 5

ONE_BACKUP_DEFENSE = 25
DEATH_ANIMATION_TICKS = 3
SOTE_RUN_UP_TICKS = 10
TIME_TO_TELEPORT_TO_MAZE_START_TICKS = 4  # this includes the 1 tick the player is "frozen"
TIME_TO_RUN_MAZE_TICKS = 11
GOOD_TICK_TO_RUN_MAZE = 3

trials = 10000
METHOD = 2
START_INSTANCE_TICK = 0

DEBUG = False

# to test:
# 0) horn w/ 4 zcb
# melee 1 is 23, melee 2 is horn + 12 (surge only)
# range is maul p1 and p3
# other 2 players zcb p1 and p3

# 1) no horn w/ 5 zcb
# melee 1 is 23, melee 2 123 (preaches+surge+lb)
# range is maul p1 and zcb p3
# other 2 players are zcb p1 and p3

# 2) 6 zcb
# melees are 123 (preach+surge+lb)
# other 3 players zcb p1 and p3

# 3) Horn P1 + 5 zcb
# Mages zcb p1 and p3 (preach and surge)
# Range Maul P1 zcb P3 (preach only)
# Melee 1 horns P1, then maul specs 23 (surge only)
# Melee 2 is 23

# 4) Horn P1 + 6 Zcb
# Mages and Range zcb p1 and p3 (preach and surge)
# Melee 1 horns P1, then maul specs 23 (surge only)
# Melee 2 is 123 (surge + preach + lb)


def main():
    times = np.empty(trials)
    p1Times = np.empty(trials)
    p2Times = np.empty(trials)
    p3Times = np.empty(trials)
    for x in range(trials):
        times[x], phaseTimes = killSote()
        p1Times[x] = phaseTimes[0]
        p2Times[x] = phaseTimes[1]
        p3Times[x] = phaseTimes[2]

    p1Times = sorted(p1Times)
    # 19.2 seconds is 32 ticks
    # 22.2 seconds is 37 ticks
    # 25.2 seconds is 42 ticks
    countFaster19 = 0
    count19 = 0
    count22 = 0
    count25 = 0
    countSlower25 = 0
    for time in p1Times:
        if time == 32:
            count19 += 1
        elif time == 37:
            count22 += 1
        elif time == 42:
            count25 += 1
        elif time < 32:
            countFaster19 += 1
        elif time > 42:
            countSlower25 += 1

    print("Percent of faster than 19.2 P1: ", countFaster19 / len(p1Times) * 100, "%")
    print("Percent of 19.2 P1: ", count19 / len(p1Times) * 100, "%")
    print("Percent of 22.2 P1: ", count22 / len(p1Times) * 100, "%")
    print("Percent of 25.2 P1: ", count25 / len(p1Times) * 100, "%")
    print("Percent of slower than 25.2 P1: ", countSlower25 / len(p1Times) * 100, "%")

    modeDisplayTimeP1 = ticksToTime(mode(p1Times))
    print("Mode: ", modeDisplayTimeP1)

    modeDisplayTimeP2 = ticksToTime(mode(p2Times))
    print("Mode: ", modeDisplayTimeP2)

    modeDisplayTimeP3 = ticksToTime(mode(p3Times))
    print("Mode: ", modeDisplayTimeP3)

    if METHOD == 0:
        plotTitle = "Sote: Horn + 4 ZCB"
    elif METHOD == 1:
        plotTitle = "Sote: No Horn + 5 ZCB"
    elif METHOD == 2:
        plotTitle = "Sote: No Horn + 6 ZCB"
    elif METHOD == 3:
        plotTitle = "Sote: Horn + 5 ZCB (1 maul p1)"
    elif METHOD == 4:
        plotTitle = "Sote: Horn + 6 ZCB (1 maul p1)"
    else:
        plotTitle = ""
        print("Invalid Method Number")
        exit(0)

    times = sorted(times)
    printStats(times)
    plotTimes(times, plotTitle, 6)
    #plotTimes(p1Times, "P1 " + plotTitle, 6)


def killSote():
    sote = Sote(SOTE_HP, SOTE_DEF, SOTE_SLASH_DEF, SOTE_CRUSH_DEF, SOTE_STANDARD_RANGE_DEF, SOTE_HEAVY_RANGE_DEF)

    roomTimeTicks = 0

    # method 1) horn + 4 zcb
    # player 0 is maul p1 and p3
    # player 1 and 2 is zcb p1 and p3 (preach and surge pot)
    # player 3 is 23
    # player 4 is horn + 12 (surge pot only)
    # playerSpecs = [100, 130, 130, 100, 125]
    # TODO spec not regening during maze so the players zcbing don't have enough spec
    if METHOD == 0:
        plotTitle = "Sote: Horn + 4 ZCB"
        playerSpecs = [100, 150, 150, 100, 125]
        playerIsWearingLb = [False, False, False, False, False]
        maulP1 = [0, 4]
        maulP2 = [3, 4]
        maulP3 = [0, 3]

        zcbP1 = [1, 2]
        zcbP2 = []
        zcbP3 = [1, 2]

        HORN = True

    # method 2) no horn + 5 zcb
    # player 0 is maul p1 and zcb p3
    # player 1 and 2 is zcb p1 and p3 (preach and surge pot)
    # player 3 is 23
    # player 4 is 123 (preach + surge + lb)
    # playerSpecs = [100, 130, 130, 100, 130]
    elif METHOD == 1:
        plotTitle = "Sote: No Horn + 5 ZCB"
        playerSpecs = [125, 150, 150, 100, 150]
        playerIsWearingLb = [False, False, False, False, True]

        maulP1 = [0, 4]
        maulP2 = [3, 4]
        maulP3 = [3, 4]

        zcbP1 = [1, 2]
        zcbP2 = []
        zcbP3 = [0, 1, 2]

        HORN = False

    # # method 3) no horn + 6 zcb
    # # player 0, 1, and 2 are zcb p1 and zcb p3 (preach and surge pot)
    # # player 3 and 4 are 123 (preach + surge + lb)
    # playerSpecs = [130, 130, 130, 130, 130]
    elif METHOD == 2:
        plotTitle = "Sote: No Horn + 6 ZCB"
        playerSpecs = [150, 150, 150, 150, 150]
        playerIsWearingLb = [False, False, False, True, True]

        maulP1 = [3, 4]
        maulP2 = [3, 4]
        maulP3 = [3, 4]

        zcbP1 = [0, 1, 2]
        zcbP2 = []
        zcbP3 = [0, 1, 2]

        HORN = False

    # 3) Horn P1 + 5 zcb
    # Mages zcb p1 and p3 (preach and surge)
    # Range Maul P1 zcb P3 (preach only)
    # Melee 1 horns P1, then maul specs 23 (surge only)
    # Melee 2 is 23
    elif METHOD == 3:
        plotTitle = "Sote: Horn + 5 ZCB"
        playerSpecs = [150, 150, 150, 150, 150]
        playerIsWearingLb = [False, False, False, False, False]

        maulP1 = [0]
        maulP2 = [3, 4]
        maulP3 = [3, 4]

        zcbP1 = [1, 2]
        zcbP2 = []
        zcbP3 = [0, 1, 2]

        HORN = True

    # 4) Horn P1 + 6 Zcb
    # Mages and Range zcb p1 and p3 (preach and surge)
    # Melee 1 horns P1, then maul specs 23 (surge only)
    # Melee 2 is 123 (surge + preach + lb)
    elif METHOD == 4:
        plotTitle = "Sote: Horn + 6 ZCB"
        playerSpecs = [150, 150, 150, 150, 150]
        playerIsWearingLb = [False, False, False, False, True]

        maulP1 = [4]
        maulP2 = [3, 4]
        maulP3 = [3, 4]

        zcbP1 = [0, 1, 2]
        zcbP2 = []
        zcbP3 = [0, 1, 2]

        HORN = True
    else:
        print("Invalid Method Number")
        exit(0)

    phaseTimes = []

    for phase in range(3):
        # reset cool downs between phases
        playerTicks = [0, 0, 0, 0, 0]
        thrallTicks = [0, 0, 0, 0, 0]

        if phase == 0:
            roomTimeTicks += SOTE_RUN_UP_TICKS
            mauls = maulP1
            zcbs = zcbP1
            phaseEndHp = SOTE_HP * 0.666
            getPreFireDamage(sote)
            calculateVengDamage(sote, 2)
            # this accounts for the players who are NOT mauling losing a tick to be on the correct tick to flinch
            for player in range(TEAM_SIZE):
                if player not in maulP1:
                    playerTicks[player] = 1

        elif phase == 1:
            # the player in the maze is 2 ticks behind
            playerInMaze = randrange(TEAM_SIZE)
            playerTicks[playerInMaze] = 2
            sote.setDefense(SOTE_DEF)  # defense resets each phase
            mauls = maulP2
            zcbs = zcbP2
            sote.setExactHp(phaseEndHp)  # you cannot overkill a phase, so the starting hp is the last phases's end hp
            phaseEndHp = SOTE_HP * 0.333
            calculateVengDamage(sote, 1)
        else:
            # the player in the maze is 2 ticks behind
            playerInMaze = randrange(TEAM_SIZE)
            playerTicks[playerInMaze] = 2
            mauls = maulP3
            zcbs = zcbP3
            sote.setExactHp(phaseEndHp)  # you cannot overkill a phase, so the starting hp is the last phases's end hp
            phaseEndHp = 0
            calculateVengDamage(sote, 1)

        if DEBUG:
            print("phase: ", phase)

        while sote.getHp() > phaseEndHp:
            roomTimeTicks += 1
            for player in range(TEAM_SIZE):
                tick = playerTicks[player]
                # if tick (aka cool down) is 0, the player can perform an attack
                if tick == 0:
                    # if this player mauls this phase
                    if playerSpecs[player] >= 50 and player in mauls:
                        mauls.remove(player)
                        # maul specs
                        if HORN and phase == 0:
                            # horn guarantees a hit lands
                            sote.getHornedMaulHit()
                        else:
                            sote.getMaulHit()

                        if DEBUG:
                            print("mauling!!!")

                        if HORN and player == 4:
                            # if we used the horn, and player 0 specs, drain all their spec
                            playerSpecs[player] -= 75
                        else:
                            # otherwise a maul spec only takes 50% spec
                            playerSpecs[player] -= WeaponConstants.maulSpecPercent

                        # set the weapon cool down for this player
                        playerTicks[player] = WeaponConstants.maulCoolDown

                    # if this player zcbs this phase
                    elif playerSpecs[player] >= WeaponConstants.zcbSpecPercent \
                            and player in zcbs \
                            and roomTimeTicks > 15:  # TODO find the actual time
                        zcbs.remove(player)
                        sote.getZcb()
                        playerSpecs[player] -= 75
                        playerTicks[player] = WeaponConstants.zcbCoolDown

                        if DEBUG:
                            print("zcbing!!!")

                    # otherwise just scythe
                    else:
                        if playerIsWearingLb[player]:
                            sote.getScytheLb()
                        else:
                            sote.getScytheUltor()
                        playerTicks[player] = WeaponConstants.scytheCoolDown

                else:
                    playerTicks[player] -= 1

                    # spec regen
                    # if this player is wearing a LB, regen spec every 25 ticks
                    if playerIsWearingLb[player] and roomTimeTicks % 25 == 0:
                        # add 10 spec, and swap rings
                        playerSpecs[player] += 10
                        playerIsWearingLb[player] = False

                    # if this player is not wearing a LB, and regen spec every 50 ticks
                    elif not playerIsWearingLb[player] and roomTimeTicks % 50 == 0:
                        playerSpecs[player] += 10

            # thrall damage
            for thrall in range(len(thrallTicks)):
                tick = thrallTicks[thrall]
                if tick == 0:
                    sote.getThrallDamage()
                    thrallTicks[thrall] = WeaponConstants.thrallCoolDown
                else:
                    thrallTicks[thrall] -= 1

        if phase == 2:
            roomTimeTicks += DEATH_ANIMATION_TICKS
        phaseTimes.append(roomTimeTicks)

        if DEBUG:
            roomTimeSeconds = roomTimeTicks * 0.6
            print("Phase " + str(phase) + " time: " + str(roomTimeSeconds) + " seconds")

        # when the phase is over, run the maze if its phase 0 or 1
        if phase == 0 or phase == 1:
            roomTimeTicks += findTimeToRunMaze(roomTimeTicks)

    return roomTimeTicks + DEATH_ANIMATION_TICKS, phaseTimes


def getPreFireDamage(sote):
    sote.getTbowTorva()
    sote.getTbowTorva()
    sote.getTbowVoid()
    sote.getTbowMasori()
    sote.getTbowMasori()


def calculateVengDamage(sote, numberOfVengsPerPerson):
    numberOfVengs = TEAM_SIZE * numberOfVengsPerPerson
    for x in range(numberOfVengs):
        sote.getVengDamage(SOTE_MAX_HIT)


def findTimeToRunMaze(roomTimeTicks):
    # 3 ticks to teleport to the start of the maze
    # 1 ticks where the player is frozen and cannot move
    timeToRunMaze = TIME_TO_TELEPORT_TO_MAZE_START_TICKS
    instanceTick = findInstanceTick(roomTimeTicks)

    # X amount of ticks to wait to run on the "good" tick
    timeToWaitTicks = 0
    while instanceTick != GOOD_TICK_TO_RUN_MAZE:
        timeToWaitTicks += 1
        instanceTick = findInstanceTick(roomTimeTicks + timeToWaitTicks)
    timeToRunMaze += timeToWaitTicks

    # 11 ticks to run across the maze
    timeToRunMaze += TIME_TO_RUN_MAZE_TICKS
    return timeToRunMaze


def findInstanceTick(roomTimeTicks):
    # it takes 1 tick to walk through the gate, and the room timer does not start until the player is completely
    # through the gate
    instanceTick = roomTimeTicks + START_INSTANCE_TICK + 1
    return instanceTick % 4


if __name__ == "__main__":
    main()
