import random, sys
from itertools import product
from scsa import *
from player import *
from mastermind import *
class Player:
    """Player for Mastermind
    """

    def __init__(self):
        """Constructor for Player
        """

        self.player_name = ""

    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chr): Colors that could be used in the secret code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret 
                                           code for the previous guess and the second element is the number of pegs that are 
                                           the right color, but in the wrong location for the previous guess.

        Raises:
            NotImplementedError: Function must be implemented by children classes.
        """

        raise NotImplementedError

class B1Player(Player):
    """Baseline 1 mastermind player
    B1: Exhaustively enumerate all possibilities. Guess each possibility in lexicographic 
    order one at a time, and pay no attention to the system’s responses. For example, if 
    pegs p = 4 and colors c = 3, guess AAAA, AAAB, AAAC, AABA, AABB, AABC and so on. 
    This method will take at most cp guesses.
    """
    def __init__(self):
        self.player_name = "Baseline1"
        self.current_guess = -1 #  index of the guess that will be made next from all_possibilities
        self.all_possibilities = []

    def next_guess(self, board_length, colors):
        # If no guesses have been made, generate all_possibilities
        if self.current_guess == -1:
            colors = ''.join(colors)
            self.all_possibilities = [''.join(p) for p in product(colors, repeat=board_length)]
            self.current_guess = 0
        else:
            if self.current_guess == len(self.all_possibilities) - 1:
                self.current_guess = 0
            else:
                self.current_guess += 1

    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chrs): Colors that could be used in the secret code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret 
                                           code for the previous guess and the second element is the number of pegs that are 
                                           the right color, but in the wrong location for the previous guess.

        Returns:
            str: Returns guess
        """
        if last_response[2] == 0:
            self.all_possibilities = []
            self.current_guess = -1
        self.next_guess(board_length, colors)
        return self.all_possibilities[self.current_guess]

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

    elif player_name == "Baseline1":
        player = B1Player()

    else:

        print("Unrecognized player.")
        sys.exit(1)


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

    colors = [chr(i) for i in range(65,91)][:num_colors]

    mastermind = Mastermind(board_length, colors)

    mastermind.play_tournament(player, scsa, num_rounds)

if __name__ == "__main__":
    main()