from Monster import Monster

horn = False
defence = 250
slash_def = 60


def main():
    mob = Monster(10000, defence, slash_def, 0, 0, 0)
    total_dmg = 0
    spec_count = 0
    while mob.getHp() > 0:
        spec_count += 1
        if horn:
            total_dmg += mob.getHorendClaw()
        else:
            total_dmg += mob.getClaw()

    average_claw = total_dmg / spec_count
    print("Average Claw: ", average_claw)


if __name__ == "__main__":
    main()
