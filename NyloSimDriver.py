import GearSets
from Player import Player

def main():
    trials = 10000


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