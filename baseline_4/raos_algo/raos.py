from player import *

class RaosAlgorithm(Player):
    def __init__(self):
        self.player_name = "RaosAlgorithm"
        self.inferences = []
        self.being_considered = None
        self.being_fixed = None
    
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




def Getnext(trial, inferences, being_considered, being_fixed):
    """
    Returns next guess

    Parameters
    ----------
    trial - Previous guess
    inferences - Knowledge base
    being_considered - Color that is being considered to see if it is part of the code
    being_fixed - Color that has been determined to be part of the code and now trying to find the right position
    """
    


def Try(trial):
    print(f"My Next Trial: {trial}")
    print("Enter Bulls >> ", end="")
    bulls = input()
    print("Enter Cows >> ", end="")
    cows = input()
    return bulls, cows

def MasterMind(N,M):
    """
    MasterMind main method

    Parameters
    ----------
    N - Number of positions/board size
    M - Number of colors
        Colors are represented as (1, 2, ..., M)
    """
        
    trial = []
    inferences = []
    being_considered = "A"
    being_fixed = None
    # setup() TODO, inialize first trial, reset knowledge base
    bulls = 0
    cows = 0
    bulls, cows = Try(trial)
    gameover = False
    while bulls < N and not gameover:
        #Update(inferences) (updates inferences based on number of bulls, cows, and previous trial)
        #Getnext(trial, inferences, Being-Considered, Being-Fixed) (updates trial based on new inferences)
        #if Numfix(inferences) == N: (goal test)
            #gameover = True
        # else:
            #  Try(trial)    
    print(trial)
def main():
    help(MasterMind)

if __name__ == "__main__":
    main()