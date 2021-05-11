from player import *
from enum import IntEnum

class KB(IntEnum):
    Color = 0
    Positions = 1


class FBI(Player):
    def __init__(self):
        self.player_name = "FBI"

        # inferences[i][0] is a color, inferences[i][1] is a list of possible positions for that color
        self.inferences = []

        # increase once every turn to try a different color
        self.being_considered = "A"

        # initial value to correspond to first color determined to be in the code
        # increase once a position is fixed for a color
        self.being_fixed = -1

        # set of positions that have been fixed
        # used set because it performs better than list when determing if an object is present within the data structure
        self.fixed = set()

        # becomes true once first bull is encountered
        self.first_bull = False 

    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chr): Colors that could be used in the secret code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret
            code for the previous guess and the second element is the number of pegs that are
            the right color, but in the wrong location for the previous guess. The third element
            it the number of guesses made so far.
        """
        # Reset
        if last_response[2] == 0:
            self.inferences = []
            self.being_considered = "A"
            self.being_fixed = -1
            self.fixed = set()
            self.first_bull = False

        # Skip updating if no guesses have been made
        if last_response[2] != 0: 
            self.update(last_response, board_length, colors)

        guess = self.get_next(board_length, colors)

        return guess
 
    def get_next(self, board_length, colors):
        """
        Returns next guess

        Parameters
        ----------
        board_length - Number of pegs of secret code
        colors - Colors that could be used in the secret code
        """
        new_trial = []

        if len(self.inferences) == board_length and len(self.fixed) != board_length:
            # Set being considered to second_unfixed
            self.second_unfixed(board_length) 

        for i in range(board_length):
            if self.tied(i):
                new_trial.append(self.its_color(i))

            elif self.being_fixed < len(self.inferences) and i == self.next_pos(self.being_fixed):
                new_trial.append(self.inferences[self.being_fixed][KB.Color])

            else:
                new_trial.append(self.being_considered)

        return ''.join(new_trial)

    def tied(self, pos):
        """
        Returns if the given position in the guess is tied to a specific color

        Parameters
        ----------
        pos - The given position in the trial/guess
        """
        if pos in self.fixed:
            return True

        return False

    def its_color(self, tied_pos):
        """
        Returns the color that a tied position is tied to

        Parameters
        ----------
        tied_pos - the position in the trial that is tied to a color
        """
        for i in range(len(self.inferences)):
            # See if this entry from inferences only has one position in possible positions
            # If position matches the tied_pos, return the color that the position is tied to
            if len(self.inferences[i][KB.Positions]) == 1 and self.inferences[i][KB.Positions][0] == tied_pos:
                return self.inferences[i][KB.Color]

    def next_pos(self, being_fixed):
        """
        Returns the next possible position for the color that is being fixed

        Parameters
        ----------
        being_fixed - the position in the trial that is tied to a color
        """
        if being_fixed == -1:
            return -1

        return self.inferences[being_fixed][KB.Positions][0]

    def second_unfixed(self, board_length):
        """
        Returns the second color that hasn't been fixed after the color being_fixed

        Parameters
        ----------
        board_length - number of positions in the code
        """
        if len(self.fixed) == board_length - 1:
            self.being_considered = self.inferences[self.being_fixed][KB.Color]
            return

        scnd_unfixed = self.being_fixed + 1
        if scnd_unfixed >= len(self.inferences):
            self.being_considered = self.inferences[self.being_fixed][KB.Color]
            return

        while self.inferences[scnd_unfixed][KB.Color] == self.inferences[self.being_fixed][KB.Color] or len(self.inferences[scnd_unfixed][KB.Positions]) == 1:
            scnd_unfixed += 1

            if scnd_unfixed >= len(self.inferences):
                self.being_considered = self.inferences[self.being_fixed][KB.Color]
                return

        self.being_considered = self.inferences[scnd_unfixed][KB.Color]


    def update(self, last_response, board_length, colors):
        """
        update method updates inferences
        Helper Functions:
            - self.fix(being_fixed)
                - 'Fix'es the beingfixed in its next possible position and deletes appropriate position from other lists.
            - self.bump(being_fixed)
                - updated the beingfixed value

        """
        bulls, cows, guesses = last_response


        if(self.being_fixed == -1):
            # if no elements have been added to the inferences, there will be no self.fixed and nothing being_fixed
            gain = (bulls+cows)
        else:
            # there is at least one color in inferences and it is being fixed

            # len(self.fixed) because those wil always return bulls that dont indicate a new color, 
            # and -1 for the colors which we are fixing since it will always return a bull or cow
            gain = (bulls+cows) - len(self.fixed)
            if self.being_fixed < len(self.inferences):
                gain -= 1 

        # add positions to inferences here
        # if gain was 0, no positions or elements will be added
        if len(self.inferences) != board_length:
            self.addlists(gain, board_length)

        if self.first_bull:
            # Prevent the inner if statements from running if we haven't found any colors of the code
            if cows == 0:
                # Fix the color being fixed to its current position
                if self.being_fixed != -1:
                    if self.being_fixed < len(self.inferences) - gain:
                        self.fix()
                        if self.being_fixed < len(self.inferences):
                            self.bump()

            elif cows == 1:
                # delete current position of being_fixed
                if(self.being_fixed != -1):
                    self.delete(0)

            elif cows == 2:
                # fix the color being considered to the current position of being fixed
                self.fix_1()

            else:
                print("Cows:", cows, self.inferences)

        # Remove excess positions from inferences
        self.clean_up()
        # Set being considered to next color
        self.next_color()

        if not self.first_bull and bulls > 0:
            self.first_bull = True

    def addlists(self, gain, board_length):
        """
        Adds new lists to inferences for the current color being_considered

        Parameters
        ----------
        gain - how many lists to add
        board_length - number of positions in code
        """
        # prepare a list item, which is a color and list of all colors*
        # add that color for the number of range(gain)
        # adding extra positions is okay here. it is taken care of by clean_up
        for i in range(gain):
            list_item = [self.being_considered, list(range(0, board_length))] 
            self.inferences.append(list_item)

        # when items are added on the list for the first time, increase self.being_fixed
        if self.being_fixed == -1 and gain != 0:
            self.bump()

    def fix(self):
        """
        Sets a certain color's positions to just its current position

        """
        if self.being_fixed >= len(self.inferences):
            return

        fixed_position = [self.inferences[self.being_fixed][KB.Positions][0]] # list with first position
        self.inferences[self.being_fixed][KB.Positions] = fixed_position
        self.fixed.add(fixed_position[0])

    def bump(self):
        """
        Finds the positions of next value that needs to be fixed in inferences

        """
        self.being_fixed = self.being_fixed+1 
        if self.being_fixed >= len(self.inferences):
            return

        while len(self.inferences[self.being_fixed][KB.Positions]) == 1:
            self.being_fixed += 1
            if self.being_fixed == len(self.inferences):
                return

    def delete(self, i):
        """
        Removes the position at index i of the color being_fixed

        Parameters
        ----------
        i - index of position in positions of being_fixed
        """
        if self.being_fixed >= len(self.inferences):
            return

        del self.inferences[self.being_fixed][KB.Positions][i] 

        if len(self.inferences[self.being_fixed][KB.Positions]) == 1:
            self.fixed.add(self.inferences[self.being_fixed][KB.Positions][0])
            self.bump()

    def fix_1(self):
        """
        Fixes the position of the color being_considered to the current position of the color being_fixed

        """
        if self.being_fixed >= len(self.inferences):
            return

        fixed_position = [self.inferences[self.being_fixed][KB.Positions][0]]

        # Find position of color being considered aka first occurences of being_considered in self.inferences that isn't fixed
        for i in range(len(self.inferences)):
            if self.inferences[i][KB.Color] == self.being_considered and len(self.inferences[i][KB.Positions]) != 1:
                idx = i
                break
            
        self.inferences[idx][KB.Positions] = fixed_position 
        self.fixed.add(fixed_position[0])


    def clean_up(self):
        """
        Removes positions that have been fixed from possible positions for all colors
        """
        for i in range(len(self.inferences)):
            if(len(self.inferences[i][KB.Positions]) != 1):
                self.inferences[i][KB.Positions] = [x for x in self.inferences[i][KB.Positions] if x not in self.fixed]
                if len(self.inferences[i][KB.Positions]) == 1 and self.inferences[i][KB.Positions][0] not in self.fixed:
                    # changed
                    self.fixed.add(self.inferences[i][KB.Positions][0])
                    if i == self.being_fixed:
                        self.bump()


    def next_color(self):
        """
        Gets the next color to consider
        """
        "should return next color to consider"
        self.being_considered = chr(ord(self.being_considered)+1)