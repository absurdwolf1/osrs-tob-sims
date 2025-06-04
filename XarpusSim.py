from Monster import Monster
from PrintTobStats import *
import numpy as np
import WeaponConstants


XARPUS_HP = 6000
XARPUS_DEF = 250

ONE_BACKUP_DEFENSE = 25
EXHUME_PHASE_TICKS = 96
DEATH_ANIMATION_TICKS = 4
EXHUME_OFFSET_PERCENT = 0.82

trials = 10000

HORN = False

if HORN:
    PLOT_TITLE = "Horn w/ 5 ZCB"
else:
    PLOT_TITLE = "Xarpus 6 ZCB"


def main():
    times = np.empty(trials)
    for x in range(trials):
        times[x] = killXarpus()

    times = sorted(times)
    printStats(times)

    below202 = len([x for x in times if x <= 206])
    above205 = len([x for x in times if x >= 209])
    at204 = len([x for x in times if 209 > x > 206])

    print("Percent Times 203 and under: ", round(below202 / trials, 2) * 100, " %")
    print("Percent Times at 204: ", round(at204 / trials, 2) * 100, " %")
    print("Percent Times 205 and higher: ", round(above205 / trials, 2) * 100, " %")

    plotTimes(times, PLOT_TITLE, 0)


def killXarpus():
    xarpus = Monster(EXHUME_OFFSET_PERCENT * XARPUS_HP, XARPUS_DEF, 0, 0, 160)

    roomTimeTicks = 0

    # player 0 is HORN (or MAUL and ZCB)
    # player 1 and 2 are MAUL and ZCB (preach)
    # player 3 is DOUBLE ZCB (preach and surge)
    # player 4 is BGS ZCB (preach)
    if HORN:
        player1Spec = 100
    else:
        player1Spec = 105

    # 105 spec represents preaching before the room
    # 130 spec represents preaching before the room and using the surge potion
    playerSpecs = [player1Spec, 105, 105, 130, 105]

    maul = [0, 1, 2]

    playerTicks = [0, 0, 0, 0, 0]
    thrallTicks = [0, 0, 0, 0, 0]

    # everyone needs to regen once using LB
    # the only exception is if player 0 is using the horn
    playerIsWearingLb = [not HORN, True, True, True, True]

    while xarpus.getHp() > 0:
        roomTimeTicks += 1
        for player in range(len(playerTicks)):
            tick = playerTicks[player]
            # if tick (aka cool down) is 0, the player can perform an attack
            if tick == 0:

                # if this player is 0, 1, or 2 (aka one of the maul roles)
                if playerSpecs[player] >= 100 and player in maul:
                    # maul specs
                    if HORN:
                        # horn guarantees a hit lands
                        xarpus.getHornedMaulHit()
                    else:
                        xarpus.getMaulHit()
                    if HORN and player == 0:
                        # if we used the horn, and player 0 specs, drain all their spec
                        playerSpecs[player] -= 100
                    else:
                        # otherwise a maul spec only takes 50% spec
                        playerSpecs[player] -= WeaponConstants.maulSpecPercent
                    # set the weapon cool down for this player
                    playerTicks[player] = WeaponConstants.maulCoolDown

                # if this player is player 4, and:
                # they have more than 50% spec, and:
                # Xarpus's defence is greater than the backup threshold
                elif playerSpecs[player] >= WeaponConstants.bgsSpecPercent \
                        and player == 4 \
                        and xarpus.getDefense() > ONE_BACKUP_DEFENSE:
                    # bgs specs
                    xarpus.getBgs()
                    playerTicks[player] = WeaponConstants.bgsCoolDown
                    playerSpecs[player] -= WeaponConstants.bgsSpecPercent
                    # if this player used both their specs, take off LB
                    if playerSpecs[player] < WeaponConstants.bgsSpecPercent:
                        playerIsWearingLb[player] = False

                # if player 3 has a bgs spec, and has to backup
                elif playerSpecs[player] >= WeaponConstants.bgsSpecPercent \
                        and player == 3 \
                        and xarpus.getDefense() > ONE_BACKUP_DEFENSE \
                        and playerSpecs[4] < 50:
                    xarpus.getBgs()
                    playerTicks[player] = WeaponConstants.bgsCoolDown
                    playerSpecs[player] -= 50
                    if playerSpecs[player] < 50:
                        playerIsWearingLb[player] = False

                # if this player has a zcb spec (and is not the double ZCB role) OR:
                # IS the double ZCB role and 1) has spec and 2) has done at least 3 scythe hits
                elif playerSpecs[player] >= 75 \
                        and player is not 3 \
                        or (playerSpecs[player] >= 75 and player == 3 and roomTimeTicks >= 15):
                    # zcb specs
                    xarpus.getZcb()
                    playerSpecs[player] -= 75
                    playerTicks[player] = WeaponConstants.zcbCoolDown

                # otherwise just scythe Xarpus
                else:
                    # scythe
                    if playerIsWearingLb[player]:
                        xarpus.getScytheLb()
                    else:
                        xarpus.getScytheUltor()
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
                xarpus.getThrallDamage()
                thrallTicks[thrall] = WeaponConstants.thrallCoolDown
            else:
                thrallTicks[thrall] -= 1

    return roomTimeTicks + EXHUME_PHASE_TICKS + DEATH_ANIMATION_TICKS


if __name__ == "__main__":
    main()
