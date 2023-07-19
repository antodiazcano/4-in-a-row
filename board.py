from typing import List, Tuple
import matplotlib.pyplot as plt



N = 4
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2



class Board:
    
    
    """ Class to represent a board for n in a row. """
    
    
    def __init__(self) -> None:
        
        """
        Constructor of the class.
        
        Parameters
        ----------
        n : Size of the board.
        """
        
        self.n = N
        self.board = [[EMPTY for _ in range(self.n)] for _ in range(self.n)]
                    
        
    def add_piece(self, i: int, j: int, piece: int) -> None:
        
        """
        Adds a piece to the board to the position (i, j) if it is empty.
        
        Parameters
        ----------
        i, j  : Position where we want to put the piece.
        piece : Player 1 or 2.
        """
        
        if self.board[i][j] == EMPTY:
            self.board[i][j] = piece
    
    
    def win(self, piece: int) -> bool:
        
        """
        Checks if a player has won.
        
        Parameters
        ----------
        piece : Player 1 or 2.
        
        Returns
        -------
        True if the player has won False otherwise.
        """
        
        # Horizontal
        for i in range(self.n):
            if self.board[i].count(piece) == self.n:
                return True
        
        # Vertical
        for i in range(self.n):
            col = [self.board[j][i] for j in range(self.n)]
            if col.count(piece) == self.n:
                return True
        
        # Positive slope diagonal
        diag = [self.board[self.n-1-i][i] for i in range(self.n)]
        if diag.count(piece) == self.n:
            return True
        
        # Negative slope diagonal
        diag = [self.board[i][i] for i in range(self.n)]
        if diag.count(piece) == self.n:
            return True
        
        return False
    
    
    def finish(self) -> bool:
         
        """
        Tells if no more pieces can be put in the board.
        
        Returns
        -------
        True if no more pieces can be put, False otherwise.
        """
        
        count = 0
        
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] == EMPTY:
                    count += 1
        
        return count == 0
    
    
    def get_valid_positions(self) -> List[Tuple[int]]:
        
        """
        Gets the positions of the board that are still empty.
        
        Returns
        -------
        List with the tuples of the coordinates that are empty.
        """
        
        return [(i, j) for i in range(self.n) for j in range(self.n)
                if self.board[i][j] == EMPTY]
    
    
    def draw(self) -> None:
        
        """
        Draws the board with matplotlib.
        """
        
        EPS = 0.1
            
        _, ax = plt.subplots()
        ax.set_aspect("equal")
        ax.set_xlim(-EPS, self.n+EPS)
        ax.set_ylim(-EPS, self.n+EPS)
        ax.axis("off")
        ax.vlines(self.n, 0, self.n, color="k")
        ax.hlines(self.n, 0, self.n, color="k")
        
        for i in range(self.n):
            ax.vlines(i, 0, self.n, color="k")
            ax.hlines(i, 0, self.n, color="k")
            for j in range(self.n):
                if self.board[i][j] == PLAYER_1: # X
                    ax.plot([j+EPS, j+1-EPS], [self.n-1-i+EPS, self.n-i-EPS],
                            color="r", linewidth=2)
                    ax.plot([j+1-EPS, j+EPS], [self.n-1-i+EPS, self.n-i-EPS],
                            color="r", linewidth=2)
                elif self.board[i][j] == PLAYER_2: # O
                    circle = plt.Circle((j+0.5, self.n-i-0.5), 0.4, color="b",
                                        linewidth=2, fill=False)
                    ax.add_artist(circle)
            
        plt.show()
        
        