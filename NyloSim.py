from Monster import Monster
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

backup = True
bgs = True
bgsHit = -1
defThreshold = 15

trials = 1


def main():
    totalTime = 0
    fastestTime = 1000000000
    totalMeleePhases = 0
    totalRangePhases = 0
    totalMagePhases = 0
    times = []
    for x in range(trials):
        timeToKill, meleePhases, rangePhases, magePhases = killNylo()
        totalTime += timeToKill
        times.append(timeToKill)
        totalMeleePhases += meleePhases
        totalRangePhases += rangePhases
        totalMagePhases += magePhases
        if fastestTime > timeToKill:
            fastestTime = timeToKill

    averageTimeSeconds = totalTime / trials
    averageMeleePhases = totalMeleePhases / trials
    averageRangePhases = totalRangePhases / trials
    averageMagePhases = totalMagePhases / trials

    averageTimeDisplayMinutes = floor(averageTimeSeconds / 60)
    averageTimeDisplaySeconds = round(averageTimeSeconds % 60, 2)
    print("Average Time: ", averageTimeDisplayMinutes, " minutes and ", averageTimeDisplaySeconds, "seconds")

    print("Mode: ", mode(times), " seconds")
    print("Std Dev:", round(stdev(times), 2), " seconds")

    print("Average Melee Phases: ", averageMeleePhases)
    print("Average Range Phases: ", averageRangePhases)
    print("Average Mage Phases: ", averageMagePhases)

    averageTotalPhases = averageMeleePhases + averageRangePhases + averageMagePhases
    print("Average Total Phases: ", averageTotalPhases)

    fastestTimeDisplayMinutes = floor(fastestTime / 60)
    fastestTimeDisplaySeconds = fastestTime % 60
    print("Fastest Time: ", fastestTimeDisplayMinutes, " minutes and ", fastestTimeDisplaySeconds, "seconds")


def killNylo():
    nylo = Nylo(NYLO_HP, NYLO_DEF, NYLO_SLASH_DEF, NYLO_CRUSH_DEF, NYLO_STANDARD_RANGE_DEF, NYLO_HEAVY_RANGE_DEF)

    phase = "melee"
    meleeCount = 1
    rangeCount = 0
    mageCount = 0

    # 1st phase is always melee
    hp -= attacks.getScytheUltor(defense)
    hp -= attacks.getScytheUltor(defense)
    hp -= attacks.getScytheUltor(defense)
    hp -= attacks.getScytheUltor(defense)

    if bgs:
        # bgs
        bgsDmg = attacks.getBgs(defense)
        if bgsHit > 0:
            bgsDmg = bgsHit
        defense = max(0, defense - bgsDmg)
        hp -= bgsDmg
    else:
        hp -= attacks.getScytheUltor(defense)

    hp -= attacks.getChally(defense)
    hp -= attacks.getChally(defense)
    hp -= attacks.getChally(defense)
    hp -= attacks.getChally(defense)

    if defense > defThreshold and backup and bgs:
        bgsDmg = attacks.getBgs(defense)
        defense = max(0, defense - bgsDmg)
        hp -= bgsDmg
    elif not bgs:
        hp -= attacks.getChally(defense)
    else:
        hp -= attacks.getClaw(defense)

    cycles = 1
    zcbSpec = True
    while hp >= 0:
        if cycles % 2 == 0:
            phase = getNyloPhase(phase)
            if phase == "melee":
                meleeCount += 1
            elif phase == "range":
                rangeCount += 1
            else:  # mage phase
                mageCount += 1

        if phase == "melee":
            for x in range(teamSize):
                attacks.getScytheUltor(defense)
        elif phase == "range":
            if rangeCount == 1 and zcbSpec:
                zcbSpec = False
                if bgs:
                    numberOfZcbs = teamSize - 1
                    hp -= attacks.getTbowTorva(defense)
                else:
                    numberOfZcbs = teamSize
                for x in range(numberOfZcbs):
                    # TODO get zcb att roll
                    hp -= attacks.getZcb(defense)
            else:
                hp -= attacks.getTbowVoid(defense)
                hp -= attacks.getTbowMasori(defense)
                hp -= attacks.getTbowMasori(defense)
                hp -= attacks.getTbowTorva(defense)
                hp -= attacks.getTbowTorva(defense)
        else:  # mage phase
            hp -= attacks.getHit(defense)
            hp -= attacks.getHit(defense)
            hp -= attacks.getHit(defense)
            hp -= attacks.getHit(defense)
            hp -= attacks.getHit(defense)

        if hp >= 0:
            cycles += 1

    totalSeconds = cycles * secondsPerCycle + deathAnimationSeconds
    return totalSeconds, meleeCount, rangeCount, mageCount


if __name__ == "__main__":
    main()
