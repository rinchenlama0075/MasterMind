from player import *
import enum


class KB(enum.Enum):
    Color = 0
    Positions = 1


class RaosAlgorithm(Player):
    def __init__(self):
        self.player_name = "RaosAlgorithm"

        # inferences[i][0] is a color, inferences[i][1] is a list of possible positions for that color
        self.inferences = []

        # increase once every turn to try a different color
        self.being_considered = 0

        # initial value to correspond to first color determined to be in the code
        # increase once a position is fixed for a color
        self.being_fixed = -1

    def make_guess(self, board_length, colors, scsa, last_response):
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list of chr): Colors that could be used in the secret code.
            scsa (SCSA): SCSA used to generate secret code.
            last_response (tuple of ints): First element in tuple is the number of pegs that match exactly with the secret 
                                           code for the previous guess and the second element is the number of pegs that are 
                                           the right color, but in the wrong location for the previous guess.
        """
        return

    def tied(self, pos):
        """
        Returns if the given position in the guess is tied to a specific color

        Parameters
        ----------
        pos - The given position in the trial/guess
        """
        for i in range(len(self.inferences)):
            # Look at each color in inferences, if the possible positions is just 1 position (tied), see if it matches the parameter pos
            # If there is a match, that position is tied to a color
            if len(self.inferences[i][KB.Positions]) == 1 and self.inferences[i][KB.Positions][0] == pos:
                return True
        return False

    def itscolor(self, tied_pos):
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

    def nextpos(self, color):
        """
       Returns the next possible position for the color 

       Parameters
       ----------
       tied_pos - the position in the trial that is tied to a color
       """

    def Getnext(self, trial):
        """
        Returns next guess

        Parameters
        ----------
        trial - Previous guess
        """
        N = len(trial)
        new_trial = []
        for i in range(N):
            if self.tied(i):
                new_trial.append(self.itscolor(i))
            elif i == self.nextpos(self.being_fixed):
                new_trial.append(self.being_fixed)
            elif len(self.inferences) == N:
                new_trial.append(secondunfixed(self.inferences))
            else:
                new_trial.append(self.being_considered)
        return new_trial

    def Try(self, trial):
        print(f"My Next Trial: {trial}")
        print("Enter Bulls >> ", end="")
        bulls = input()
        print("Enter Cows >> ", end="")
        cows = input()
        return bulls, cows


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
