from itertools import permutations
from player import Player

class Baseline3(Player):
    """ Baseline 3 mastermind player
    B3: Make your first c – 1 guesses monochromatic: "all A’s," "all B’s,"… for all but one of the c colors. That
    will tell you how many pegs of each color are in the answer. (You don't need to actually guess the last color;
    you can compute how many of those there are from the other answers.) Then you generate and test only answers
    consistent with that known color distribution. 
    """
    def __init__(self):
        self.player_name = "Baseline3"
        self.monochromatic_guess_list = []
        # Keys: color
        # Value: # of color present in the secret code
        self.color_count_dict = {} 
        self.informed_guess_list = []
        self.informed_guess_list_counter = 0
        
    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chrs): All possible colors that can be used to generate a code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret 
                                           code for the previous guess and the second element is the number of pegs that are 
                                           the right color, but in the wrong location for the previous guess.

        Returns:
            str: Returns guess
        """
        match_pegs, mismatch_pegs, num_guess = last_response
        guess = ''
        if num_guess == 0:
            # Clear values for each round
            self.informed_guess_list_counter = 0
            self.color_count_dict.clear()
            self.monochromatic_guess_list = []
            self.informed_guess_list = []

            # Makes a list of c - 1 colors
            self.monochromatic_guess_list = [ colors[i] * board_length for i in range(len(colors)-1)]
            guess = self.monochromatic_guess_list[num_guess]

        elif num_guess > 0 and num_guess <= len(self.monochromatic_guess_list):
            total_pegs_of_a_color = match_pegs + mismatch_pegs 
            
            # Keys: color
            # Value: # of color present in the secret code
            self.color_count_dict[colors[num_guess-1]] = total_pegs_of_a_color

            if num_guess == len(self.monochromatic_guess_list):
                # Calculating how times the c color appears in secret code
                values = self.color_count_dict.values()
                num_pegs_left = board_length - sum(values)
                self.color_count_dict[colors[num_guess]] = num_pegs_left

                # Generate an informed guess list based on the permutations of the color and the # of times the color appears in secret code
                informed_string = ''
                for key, value in self.color_count_dict.items():
                    informed_string += key * value
                self.informed_guess_list = [''.join(p) for p in permutations(informed_string)]
                
                # Removes duplicates in informed guess list
                self.informed_guess_list = list(set(self.informed_guess_list))
                guess = self.informed_guess_list[self.informed_guess_list_counter]

            else:
                guess = self.monochromatic_guess_list[num_guess]

        else:
            # Go through the informed guess list
            self.informed_guess_list_counter += 1
            guess = self.informed_guess_list[self.informed_guess_list_counter]

        return guess