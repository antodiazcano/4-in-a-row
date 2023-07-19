from board import Board, N, EMPTY, PLAYER_1, PLAYER_2
import numpy as np
import random
from typing import List, Tuple, Literal



def evaluate_window(window: List[int], player: int) -> int:
    
    """
    Gives a heuristic score for a window.
    
    Parameters
    ----------
    window : Window.
    player : What player is playing.
    
    Returns
    -------
    Heuristic score of the window.
    """
    
    if player == PLAYER_1:
        opp_player = PLAYER_2
    else:
        opp_player = PLAYER_1
        
    # Player winning
    if window.count(player) == 4:
        return 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        return 8
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        return 2
    # Avoid the other player winning
    elif window.count(opp_player) == 4:
        return -100
    elif window.count(opp_player) == 3 and window.count(EMPTY) == 1:
        return -8
    elif window.count(opp_player) == 2 and window.count(EMPTY) == 2:
        return -2
    # Other possibilities
    else:
        return 0
    

def score_board(board: List[List[int]], player: int) -> int:
    
    """
    Gives a heuristic score for the AI adding a piece in the position (i, j).
    
    Parameters
    ----------
    board  : Matrix representing the board.
    player : What player is playing.
    
    Returns
    -------
    score  : Heuristic score of the board.
    """

    score = 0
    
    # Rows and columns
    for i in range(N):
        score += evaluate_window(board[i], player) # row
        score += evaluate_window([board[j][i] for j in range(N)], player) # col
     
    # Diagonals
    score += evaluate_window([board[N-1-i][i] for i in range(N)], player)
    score += evaluate_window([board[i][i] for i in range(N)], player)
    
    return score
    
    
def minimax(B: Board, depth: int, alpha: float, beta: float,
            maxPlayer: bool)-> Tuple[Tuple[int], int]:
    
    """
    The AI selects a position to put the piece using minimax algorithm.
    
    Parameters
    ----------
    B           : Board where we are playing.
    depth       : Depth of the search.
    alpha, beta : Parameters for alpha-beta pruning.
    maxPlayer   : If the player wants to maximize or not.
    
    Returns
    -------
    Best position to play found and the heuristic value.
    """
    
    if depth == 0 or B.win(PLAYER_1) or B.win(PLAYER_2) or B.finish():
        if B.win(PLAYER_1):
            return (None, -100)
        elif B.win(PLAYER_2):
            return (None, 100)
        elif B.finish():
            return (None, 0)
        else:
            if maxPlayer:
                return (None, score_board(B.board, PLAYER_2))
            else:
                return (None, score_board(B.board, PLAYER_1))
    
    valid_positions = B.get_valid_positions()
        
    if maxPlayer: # AI
        value = -np.inf
        for position in valid_positions:
            temp_B = Board()
            temp_B.board = [[B.board[i][j] for j in range(N)]
                            for i in range(N)]
            temp_B.add_piece(position[0], position[1], PLAYER_2)
            new_score = minimax(temp_B, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_pos = position
            alpha = max(alpha, value)
            if value >= beta:
                break
        return (best_pos, value)
    else: # us
        value = np.inf
        for position in valid_positions:
            temp_B = Board()
            temp_B.board = [[B.board[i][j] for j in range(N)]
                            for i in range(N)]
            temp_B.add_piece(position[0], position[1], PLAYER_1)
            new_score = minimax(temp_B, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_pos = position
            beta = min(beta, value)
            if value <= alpha:
                break
        return (best_pos, value)
        

def play_game(level: Literal["easy", "medium", "hard"] = "hard") -> None:
    
    """
    Function to play a game vs the AI.
    """
    
    B = Board()
    turn = random.randint(0, 1)
    if level == "easy":
        depth = 1
    elif level == "medium":
        depth = 2
    else:
        depth = 7
    
    while not (B.win(PLAYER_1) or B.win(PLAYER_2) or B.finish()):
        
        if turn == 0: # human
            i = int(input("\nRow: "))
            j = int(input("Col: "))
            while B.board[i][j] != EMPTY:
                print("\nSelect a valid position.\n")
                i = int(input("Row: "))
                j = int(input("Col: "))
            B.add_piece(i, j, PLAYER_1)
        else: # AI
            temp_B = Board()
            temp_B.board = [[B.board[i][j] for j in range(B.n)]
                            for i in range(B.n)]
            pos = minimax(temp_B, depth, -np.inf, np.inf, True)[0]
            B.add_piece(pos[0], pos[1], PLAYER_2)
            
        B.draw()
        turn = (turn + 1) % 2
    
    if B.win(PLAYER_1):
        print("\nCongratulations, you won!")
    elif B.win(PLAYER_2):
        print("\nSorry, AI won!")
    else:
        print("\nIt is a draw!")
        
