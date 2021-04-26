# Main file to run game of Mastermind based on command-line arguments
# See example.ipynb for other ways to use the Mastermind representation

import sys
from scsa import *
from player import *
from mastermind import *
from fbi_B3 import Baseline3
# from fbi_B2 import Baseline2


def main():
    if len(sys.argv) != 6:
        print("Usage: python3 main.py <board length> <num colors> <player name> <scsa name> <num rounds>")
        sys.exit(1)

    board_length = int(sys.argv[1])
    num_colors = int(sys.argv[2])
    player_name = sys.argv[3]
    scsa_name = sys.argv[4]
    num_rounds = int(sys.argv[5])

    if player_name == "RandomFolks":

        player = RandomFolks()

    elif player_name == "Boring":

        player = Boring()

    elif player_name == "Baseline3":
        player = Baseline3()

    # elif player_name == "Baseline2":
    #     player = Baseline2()

    else:

        print("Unrecognized player.")
        sys.exit(1)

    if len(scsa_name) > 7 and scsa_name[:7] == "Mystery":
        if scsa_name == "Mystery1":

            scsa = Mystery1()
            code_file = "mystery_codes/200_codes_for_mystery1_7_5.txt"

        elif scsa_name == "Mystery2":

            scsa = Mystery2()
            code_file = "mystery_codes/200_codes_for_mystery2_7_5.txt"

        elif scsa_name == "Mystery3":

            scsa = Mystery3()
            code_file = "mystery_codes/200_codes_for_mystery3_7_5.txt"

        elif scsa_name == "Mystery4":

            scsa = Mystery4()
            code_file = "mystery_codes/200_codes_for_mystery4_7_5.txt"

        elif scsa_name == "Mystery5":

            scsa = Mystery5()
            code_file = "mystery_codes/200_codes_for_mystery5_7_5.txt"

        else:

            print("Unrecognized SCSA.")
            sys.exit(1)

        colors = [chr(i) for i in range(65, 91)][:num_colors]

        mastermind = Mastermind(board_length, colors)

        mastermind.practice_tournament(player, scsa, code_file)

    else:
        if scsa_name == "InsertColors":

            scsa = InsertColors()

        elif scsa_name == "TwoColor":

            scsa = TwoColor()

        elif scsa_name == "ABColor":

            scsa = ABColor()

        elif scsa_name == "TwoColorAlternating":

            scsa = TwoColorAlternating()

        elif scsa_name == "OnlyOnce":

            scsa = OnlyOnce()

        elif scsa_name == "FirstLast":

            scsa = FirstLast()

        elif scsa_name == "UsuallyFewer":

            scsa = UsuallyFewer()

        elif scsa_name == "PreferFewer":

            scsa = PreferFewer()

        else:

            print("Unrecognized SCSA.")
            sys.exit(1)

        colors = [chr(i) for i in range(65, 91)][:num_colors]

        mastermind = Mastermind(board_length, colors)

        mastermind.play_tournament(player, scsa, num_rounds)


if __name__ == "__main__":
    main()
