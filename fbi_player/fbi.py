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
        if last_response[2] == 0:
            self.inferences = []
            self.being_considered = "A"
            self.being_fixed = -1
            self.fixed = set()
            self.first_bull = False
        # Access guess number from last guess. Default guess number value is 0
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

    # should return based on next on inf list,can't use being fixed as index
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
        Sets being_considered to the second color that hasn't been fixed yet
        Which is useful because we call this once inferences is full
        So when we end up calling fix_1 with inferences full because 
        being_considered is not a color that isnt part of the code
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
        # if gain was 0, no positons or elements will be added
        if len(self.inferences) != board_length:
            self.addlists(gain, board_length)

        if self.first_bull: 
            if cows == 0:
                # Begin
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
                self.fix_1()
            else:
                print("Cows:", cows, self.inferences)

        self.clean_up()
        self.next_color()
        if not self.first_bull and bulls > 0:
            self.first_bull = True

    # Takeaways: We only add lists when we want to take something that is being considered and start fixing it
    def addlists(self, gain, board_length):
        # prepare a list item, which is a color and list of all colors*
        # add that color for the number of range(gain)
        # adding extra positions is okay here. it is taken care of by clean_up
        for i in range(gain):
            # Quick change I switched from passing self.being_considered as a parameter to just accessing the data member
            list_item = [self.being_considered, list(range(0, board_length))] 
            self.inferences.append(list_item)
        # when items are added on the list for the first time, increase self.being_fixed
        if self.being_fixed == -1 and gain != 0:
            self.bump()

    def fix(self):
        if self.being_fixed >= len(self.inferences):
            return
        "should put beingfixed in its possible position and deletes appropriate position from other lists"
        fixed_position = [self.inferences[self.being_fixed][KB.Positions][0]] # list with first position
        self.inferences[self.being_fixed][KB.Positions] = fixed_position
        self.fixed.add(fixed_position[0])

    def bump(self):
        "get the next beingfixed "
        self.being_fixed = self.being_fixed+1 
        if self.being_fixed >= len(self.inferences):
            return
        while len(self.inferences[self.being_fixed][KB.Positions]) == 1:
            self.being_fixed += 1
            if self.being_fixed == len(self.inferences):
                return

    # RAO'S IMPLEMENTATION
    # def delete(self, i, j):
    #     "from the sublist in inferences, delete current position of color i from the sublist of color j"
    #     self.inferences[j][KB.Positions].remove(
    #         self.inferences[i][KB.Positions][0])

    # Sensible Implementation of delete
    def delete(self, i):
        if self.being_fixed >= len(self.inferences):
            return
        # I needed this to delete by index not by value so I changed it to this
        del self.inferences[self.being_fixed][KB.Positions][i] 

        if len(self.inferences[self.being_fixed][KB.Positions]) == 1:
            self.fixed.add(self.inferences[self.being_fixed][KB.Positions][0])
            self.bump()

    # I removed parameters i and j because they are being_fixed and being_considered which are data members
    def fix_1(self):
        """
            Fix the position of the color being_considered to the current position of the color being_fixed
        """
        if self.being_fixed >= len(self.inferences):
            return

        fixed_position = [self.inferences[self.being_fixed][KB.Positions][0]]

        # index -1 works because we only enter this method if we just expanded our inferences by adding
        # rows for the color being_considered, and we want to fix the position of one of those colors
        # Since its at the end of the inferences array, -1 accesses it

        # Find position of color being considered aka first occurences of being_considered in self.inferences that isn't fixed
        for i in range(len(self.inferences)):
            if self.inferences[i][KB.Color] == self.being_considered and len(self.inferences[i][KB.Positions]) != 1:
                idx = i
                break
        self.inferences[idx][KB.Positions] = fixed_position 
        self.fixed.add(fixed_position[0])


    # Changed self.fixed into a set as the condition x not in self.fixed becomes O(1),
    # rather than O(n) with lists
    def clean_up(self):
        "remove positions that have been fixed from possible positions for all colors"
        for i in range(len(self.inferences)):
            if(len(self.inferences[i][KB.Positions]) != 1):
                self.inferences[i][KB.Positions] = [x for x in self.inferences[i][KB.Positions] if x not in self.fixed]
                if len(self.inferences[i][KB.Positions]) == 1 and self.inferences[i][KB.Positions][0] not in self.fixed:
                    # changed
                    self.fixed.add(self.inferences[i][KB.Positions][0])
                    if i == self.being_fixed:
                        self.bump()


    def next_color(self):
        "should return next color to consider"
        self.being_considered = chr(ord(self.being_considered)+1)

    # should return total num of tied positions. not all possible positions
    # return len(self.fixed)
    def num_fix(self):
        "should return the num of positions tied to colors"
        count = 0
        for x in range(len(self.inferences)):
                # print("color: ", self.inferences[x], " is tied to: ")
            for y in range(len(self.inferences[x])):
                # print(self.inferences[x][y])
                count = count+1

        return count