import random
import pandas as pd


stats = {"battles_fought": [], "wars_fought": [], "engagements": [], "war_ratio": []}


def create_deck(use_jokers=False):
    diamonds = list(range(13))
    clubs = list(range(13))
    hearts = list(range(13))
    spades = list(range(13))
    jokers = [["J", "J"] if use_jokers else []][0]

    deck = diamonds + clubs + hearts + spades + jokers
    random.shuffle(deck)

    # print(deck)
    return deck


# shuffle cards in hand


def _commit_troop(general, number_to_commit=1):
    # always retain 1 troop for engagement
    if number_to_commit > len(general["reinforcements"]) - 1:
        number_to_commit = len(general["reinforcements"]) - 1

    # todo: check to see if reinforcements
    for i in range(number_to_commit):
        general["committed"].append(general["reinforcements"].pop())
        # print(
        #     f"{general['name']}- \
        #     {general['committed']} committed/ \
        #     {len(general['reinforcements'])} reinforcements"
        # )


def _engage_troop(general):

    if general["reinforcements"]:
        general["engaged"].append(general["reinforcements"].pop())

    return general["engaged"]


def _move_troops(winner, loser, from_list, to_list):
    winner[to_list].append(loser[from_list])
    winner[to_list].append(winner[from_list])
    loser[from_list] = []
    winner[from_list] = []


def _update_stats(winner, loser, war=False):
    engagement_type = "wars" if war else "battles"

    for general in [winner, loser]:
        general[f"{engagement_type}_fought"] += 1

    winner[f"{engagement_type}_won"] += 1


def _take_the_win(winner, loser, war=False):
    # move committed if this was a war
    if war:
        _move_troops(winner, loser, "committed", "reserves")

    _move_troops(winner, loser, "engaged", "reserves")
    _update_stats(winner, loser, war)
    # check for ultimate loss
    return True


def engage_in_battle(generals, war=False):
    gen1 = generals[0]
    gen2 = generals[1]

    for general in generals:
        _commit_troop(general)

    gen1_engaged = _engage_troop(gen1)[-1]
    gen2_engaged = _engage_troop(gen2)[-1]
    enaged = [gen1_engaged, gen2_engaged]

    # Jokers are always a war
    if "J" in enaged:
        # print("Joker WAR!!")
        engage_in_battle(generals, war=True)
    if gen1_engaged == gen2_engaged:
        # print("WAR")
        # battle again, if either has reinforcements available
        if gen1["reinforcements"] or gen2["reinforcements"]:
            engage_in_battle(generals, war=True)
    # not another war
    # todo 2 beat ace?
    elif gen1_engaged > gen2_engaged:
        # print(f"{gen1['name']} wins!!")
        _take_the_win(gen1, gen2, war)
    elif gen1_engaged < gen2_engaged:
        # print(f"{gen2['name']} wins!!")
        _take_the_win(gen2, gen1, war)
    else:
        print("something wierd happened...")
        print(gen1)
        print(gen2)


# play war

# score battle


def make_general(name):
    # make user
    general = {}
    general["name"] = name
    general["reinforcements"] = create_deck()  # troops ready to do battle
    general["reserves"] = []  # troops won in battle, not reincoprated to fight yet
    general["committed"] = []  # commited to battles pending war
    general["engaged"] = []  # troop active in a battle
    general["battles_fought"] = 0
    general["battles_won"] = 0
    general["wars_fought"] = 0
    general["wars_won"] = 0
    return general


def show_stats(general):
    engagements = ["battles", "wars"]
    print(general["name"])
    for e in engagements:
        print(f"{e}: won {general[f'{e}_won']} of {general[f'{e}_fought']}")


def game_stats(gen1, stats):
    engagements = gen1["battles_fought"] + gen1["wars_fought"]
    stats["battles_fought"].append(gen1["battles_fought"])
    stats["wars_fought"].append(gen1["wars_fought"])
    stats["engagements"].append(engagements)
    stats["war_ratio"].append(gen1["wars_fought"] / engagements)

    # print(f"battles: {battles_fought}, wars: {wars_fought}, war ratio: {war_ratio}")
    return stats


def prosecute_war(stats):
    # setup game
    gen1 = make_general("Korben")
    gen2 = make_general("Matt")
    generals = [gen1, gen2]
    both_armies_exist = True

    # play game
    while gen1["reinforcements"]:
        engage_in_battle(generals)

    # for general in generals:
    #     show_stats(general)

    stats = game_stats(gen1, stats)


def main(stats):
    prosecute_war(stats)


if __name__ == "__main__":
    for i in range(1000):
        main(stats)

