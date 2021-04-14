from player import Player

class B4Player(Player):
    """Baseline 4 mastermind player
    B4: An implementation of Rao's Algorithm.

    Credit goes to T. Mahadeva Rao for their research.
    """
    def __init__(self):
        self.player_name = "Baseline4"
        self.inferences = {}
        self.last_guess = None

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
            # if a new round has begun
            return
            
        while(last_response[0]  < board_length): # While (bull < N) and (not gameover) 

def main():
    player = B4Player()
    player.make_guess(4, ["A","B","C","D","E","F"], None, (0,0,0))

if __name__ == "__main__":
    main()