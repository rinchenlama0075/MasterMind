from player import *
import enum
from main import *


class KB(enum.Enum):
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

        # list of positions that have been fixed
        self.fixed = []


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
        # should access guess number from last guess? which can be defaulted to 0
        self.update(last_response, board_length, colors)
        guess = self.get_next(board_length, colors)
        return guess

    """
    get_next method returns next guess
    Helper functions:
        - self.tied(pos)
            - Returns true if pos has a color tied to it.
        - self.its_color(tied_pos)
            - Returns the color to which tied_pos is tied to.
        - self.next_pos(being_fixed)
            - Returns the next possible position for the color being fixed, i.e. first color in possible positions
        - self.second_unfixed()
            - Returns the second color which is not yet fixed
    """

    def get_next(self, board_length, colors):
        """
        Returns next guess

        Parameters
        ----------
        trial - Previous guess
        """
        new_trial = []
        for i in range(board_length):
            if self.tied(i):
                new_trial.append(self.its_color(i))
            elif i == self.next_pos(self.being_fixed):
                new_trial.append(self.being_fixed)
            elif len(self.inferences) == board_length:
                new_trial.append(second_unfixed(self.inferences))
            else:
                new_trial.append(colors[self.being_considered])
        return new_trial

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

    # should return second pos from inf that is not fixed cant; increase being_fixed by 1
    def second_unfixed(self):
        return being_fixed + 1

    """
    update method updates inferences
    Helper Functions:
        - self.fix(being_fixed)
            - 'Fix'es the beingfixed in its next possible position and deletes appropriate position from other lists.
        - self.bump(being_fixed)

    """

    def update(self, last_response, board_length, colors):
        bulls, cows, guesses = last_response
        if guesses == 0:
            return
        if bulls == 0 and cows == 0:
            self.being_considered += 1
            return

        # if(self.being_fixed == 0):
        #     gain = (bulls+cows) - self.num_fix(self.inferences) - 1
        # else:
        #     gain = (bulls+cows) - self.num_fix(self.inferences)

        # add positions to inferences here
        # addlists
        self.addlists(self, last_response, board_length, colors)
        if cows == 0:
            # Begin
            if self.being_fixed != -1:
                self.fix(self.being_fixed)
            self.bump(self.being_fixed)
        elif cows == 1:
            if(self.being_fixed != 0):
                self.delete(self.being_fixed, self.being_considered)
            self.delete(self.being_fixed, self.being_fixed)
        elif cows == 2:
            self.fix_1(self.being_considered, self.being_fixed)
        else:
            print("error")

        self.clean_up(self.inferences)
        self.next_color()

    # Takeaways: We only add lists when we want to take something that is being considered and start fixing it
    def addlists(self, last_response, board_length, colors):
        bulls, cows, guess_number = last_response

        # Get possible positions by taking all possible positions and remove those that have been fixed
        possible_positions = list(set(range(board_length)) - set(self.fixed))

        # We have also fixed some colors which will be part of the bulls
        # we can take away that amount to be left with the number of 
        # similar to how we calculate gain, not sure why we -1 in one of the gain calculations
        num_lists_to_add = (bulls + cows) - len(self.fixed)
        for i in range(num_lists_to_add):
            inferences.append([colors[]])


    def fix(self, being_fixed):
        "should put beingfixed in its possible position and deletes appropriate position from other lists"
        for x in range(len(self.inferences[self.being_fixed][KB.Positions])-1):
            self.inferences[self.being_fixed][KB.Positions].pop(-1)
        self.fixed.append(self.inferences[self.being_fixed][KB.Positions][0])

    def bump(self, being_fixed):
        "get the next beingfixed "
        self.being_fixed = self.being_fixed+1

    def delete(self, i, j):
        "from the sublist in inferences, delete current position of color i from the sublist of color j"
        self.inferences[j][KB.Positions].remove(
            self.inferences[i][KB.Positions][0])

    def fix_1(self, i, j):
        "fix color i in the current position of color j"
        self.inferences[i][KB.Positions][0] = self.inferences[j][KB.Positions][0]
        for x in range(len(self.inferences[i][KB.Positions])-1):
            self.inferences[i][KB.Positions].pop(-1)

    def clean_up(self, inferences):
        "remove positions that have been fixed from the sublist of the color being_fixed  "
        for x in range(len(self.inferences)):
            if len(self.inferences[x][KB.Positions]) == 1:
                break
            else:
                for y in range(len(self.inferences[x])):
                    if(self.inferences[x][KB.Positions][y] in self.fixed):
                        self.inferences[x][KB.Positions].remove(
                            self.inferences[x][KB.Positions][y])

    def next_color(self):
        "should return next color to consider"
        self.being_considered = self.being_considered+1

    # should return total num of tied positions. not all possible positions
    # return len(self.fixed)
    def num_fix(self, inferences):
        "should return the num of positions tied to colors"
        count = 0
        for x in range(len(inferences)):
            # print("color: ", self.inferences[x], " is tied to: ")
            for y in range(len(inferences[x])):
                # print(self.inferences[x][y])
                count = count+1

        return count

    # def evaluate_guess(self, trial):
    #     print(f"My Next Trial: {trial}")
    #     print("Enter Bulls >> ", end="")
    #     bulls = input()
    #     print("Enter Cows >> ", end="")
    #     cows = input()
    #     return bulls, cows

# def MasterMind(N, M):
#     """
#     MasterMind main method

#     Parameters
#     ----------
#     N - Number of positions/board size
#     M - Number of colors
#         Colors are represented as (1, 2, ..., M)
#     """

#     trial = []
#     inferences = []
#     being_considered = "A"
#     being_fixed = None
#     # setup() TODO, inialize first trial, reset knowledge base
#     bulls = 0
#     cows = 0
#     bulls, cows = Try(trial)
#     gameover = False
#     while bulls < N and not gameover:
#         # Update(inferences) (updates inferences based on number of bulls, cows, and previous trial)
#         # Getnext(trial, inferences, Being-Considered, Being-Fixed) (updates trial based on new inferences)
#         # if Numfix(inferences) == N: (goal test)
#             #gameover = True
#         # else:
#             #  Try(trial)
#     print(trial)


# def main():
#     help(MasterMind)


# if __name__ == "__main__":
#     main()

# sometimes he uses ":=" to mean assignment and "=" to mean ==, but sometimes he also uses "=" to mean assignment too oh wait I mean he uses <> to mean == but will use either := or = for assignment
if __name__ == "__main__":
    main()


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

    elif player_name == "FBI":

        player = FBI()

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

    colors = [chr(i) for i in range(65, 91)][:num_colors]

    mastermind = Mastermind(board_length, colors)

    mastermind.play_tournament(player, scsa, num_rounds)
