from itertools import product
from player import Player


class Baseline2(Player):
    """Exhaustively enumerate all possibilities. 
        Guess each possibility in lexicographic order unless it was ruled out by some previous response. 
        For example, for p = 4, if guess AAAB got 0 0 1 in response, you would never again on that round make any guess that began with AAA or ended in B.
    """

    def __init__(self):
        self.player_name = "baseline_B2_fbi"
        self.last_guess = ""
        self.updated_list = []

    def next_guess(self, board_length, colors, last_response):
        # If no guesses have been made, generate all_possibilities
        # print("a response was received: " + str(last_response))
        if last_response[2] == 0:
            colors = ''.join(colors)
            self.all_possibilities = [
                ''.join(p) for p in product(colors, repeat=board_length)]
            self.updated_list = self.all_possibilities
            self.current_guess = 0
        elif(last_response[0] == 0 and last_response[1] == 0):
            x = self.updated_list
            last_guess = self.last_guess
            for i in range(5):
                noBull_nocow_remaining = [
                    x for x in self.updated_list if last_guess[i] not in x]
            self.updated_list = noBull_nocow_remaining

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
        self.next_guess(board_length, colors, last_response)
        # print(self.next_guess(board_length, colors))
        self.last_guess = self.updated_list[0]
        self.updated_list.remove(self.last_guess)
        # print("guessing: " + self.last_guess)
        return self.last_guess
