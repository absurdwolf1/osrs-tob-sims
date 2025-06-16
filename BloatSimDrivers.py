import GearSets
from Player import Player
from BloatSim import killBloat
import numpy as np
from statistics import mode
from PrintTobStats import printStatsWithPrefix


def main():
    printSeparator()

    killTimeVsDownTimeTest()
    printSeparator()

    bgsThresholdTest()
    printSeparator()

    specWeaponsTest()


def killTimeVsDownTimeTest():
    trials = 10000
    times = []
    minDown = 39
    maxDown = 49

    print("Average Kill Time vs Down Time Test")
    print("Min Down: " + str(minDown))
    print("Max Down: " + str(maxDown))
    printSeparator()

    for down in range(minDown, maxDown + 1):
        for x in range(trials):
            players = createPlayers()
            time = killBloat(players, down, -1)
            if time > 0:
                times.append(time)

        averageTimeSeconds = round(np.average(times) * 0.6, 2)
        modeSeconds = mode(times) * 0.6
        print("Down (ticks): " + str(down) + " | Average Time (seconds): " + str(averageTimeSeconds))
        print("Down (ticks): " + str(down) + " | Mode (seconds): " + str(modeSeconds))


def bgsThresholdTest():
    trials = 10000
    times = []

    print("Bgs Threshold Test")
    printSeparator()

    for bgsThreshold in range(0, 100, 5):
        for x in range(trials):
            players = createPlayers()
            time = killBloat(players, -1, bgsThreshold)
            if time > 0:
                times.append(time)

        averageTimeSeconds = round(np.average(times) * 0.6, 2)
        modeSeconds = mode(times) * 0.6
        print("Backup Threshold: " + str(bgsThreshold) + " | Average Time (seconds): " + str(averageTimeSeconds))
        print("Backup Threshold: " + str(bgsThreshold) + " | Mode (seconds): " + str(modeSeconds))


def specWeaponsTest():
    trials = 10000

    print("Zcb vs Claw vs Chally Test")

    times = []
    for x in range(trials):
        players = createPlayers()
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)
    printSeparator()
    printStatsWithPrefix(times, "All Claw")

    times = []
    for x in range(trials):
        players = createPlayers()
        players[0].setSpec(125, ["zcb", "claw"])
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)
    printSeparator()
    printStatsWithPrefix(times, "1 Zcb")

    times = []
    for x in range(trials):
        players = createPlayers()
        players[0].setSpec(125, ["zcb", "claw"])
        players[1].setSpec(125, ["zcb", "claw"])
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)
    printSeparator()
    printStatsWithPrefix(times, "2 Zcb")

    times = []
    for x in range(trials):
        players = createPlayers()
        players[0].setSpec(125, ["zcb", "claw"])
        players[1].setSpec(125, ["zcb", "claw"])
        players[2].setSpec(125, ["zcb", "claw"])
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)
    printSeparator()
    printStatsWithPrefix(times, "3 Zcb")

    times = []
    for x in range(trials):
        players = createPlayers()
        players[0].setSpec(130, ["claw", "claw", "chally"])
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)
    printSeparator()
    printStatsWithPrefix(times, "1 Chally")

    times = []
    for x in range(trials):
        players = createPlayers()
        players[0].setSpec(130, ["claw", "claw", "chally"])
        players[1].setSpec(130, ["claw", "claw", "chally"])
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)
    printSeparator()
    printStatsWithPrefix(times, "2 Chally")

    times = []
    for x in range(trials):
        players = createPlayers()
        players[0].setSpec(130, ["claw", "claw", "chally"])
        players[1].setSpec(130, ["claw", "claw", "chally"])
        players[2].setSpec(130, ["claw", "claw", "chally"])
        time = killBloat(players, -1, -1)
        if time > 0:
            times.append(time)
    printSeparator()
    printStatsWithPrefix(times, "3 Chally")


def createPlayers():
    players = []

    # NORTH MAGE
    player1 = Player()
    player1.setSpec(125, ["claw", "claw"])
    player1.setMeleeGear(GearSets.scytheOathSalve)
    player1.setRangeGear(GearSets.tbowMasori)
    players.append(player1)

    # MAGE DPS
    player2 = Player()
    player2.setSpec(125, ["claw", "claw"])
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


def printSeparator():
    print("-----------------------------------")


if __name__ == "__main__":
    main()
