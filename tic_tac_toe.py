"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.

NTRIALS = 10        # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    

# Add your functions here.

def check_who_won(winner, player1):
    """
    Helper function for update scores.
    """
    if player1 == winner:
        player_win = True
        other_win = False
        
    elif winner == provided.DRAW:
        player_win = False
        other_win = False
        
    else:
        other_win = True
        player_win = False
        
    return player_win, other_win    
        
def mc_trial(board, player):
    """
    Monte-Carlo trial, given the board and starting player.
    """
    
    win = board.check_win()
    while win == None:
        empty_squares = board.get_empty_squares()
        move = random.choice(empty_squares)
        board.move(move[0], move[1], player)
        player = provided.switch_player(player)
        win = board.check_win()
    
    return
    
def mc_update_scores(scores, board, player):
    """
    Scores the board, depending on who won or lost.
    """
    win = board.check_win()
    player_win, other_win = check_who_won(win, player)
    
    dim = board.get_dim()
     
    for _row in range(dim):
        for _col in range(dim):
            if player_win:
                if board.square(_row, _col) == player:
                    scores[_row][_col] += SCORE_CURRENT
                    
                elif board.square(_row, _col) == provided.EMPTY:
                    scores[_row][_col] += 0
                    
                else:
                    scores[_row][_col] -= SCORE_OTHER
                    
            elif other_win:
                if board.square(_row, _col) == player:
                    scores[_row][_col] -= SCORE_CURRENT
                    
                elif board.square(_row, _col) == provided.EMPTY:
                    scores[_row][_col] += 0
                    
                else:
                    scores[_row][_col] += SCORE_OTHER
                    
            elif win == provided.DRAW:   
                scores[_row][_col] += 0

def get_best_move(board, scores):
    """
    Get square with highest cumulative score as best move.
    In case of tie, pick randomly.
    """
    
    max_squares = []
    best_score = None
    squares = board.get_empty_squares()
    for square in squares:
        if scores[square[0]][square[1]] >= best_score:
            best_score = scores[square[0]][square[1]]
    max_squares = [square for square in squares if scores[square[0]][square[1]] == best_score]       
    best_move = random.choice(max_squares)
    return best_move

def mc_move(board, player, trials):
    """
    Run Monte-Carlo simulation to find out the best move and then 
    implement it.
    """
    dim = board.get_dim()
    scores_total = [[0 for dummy_col in range(dim)] for dummy_row in range(dim)]
    
    for dummy_trial in range(trials):
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(scores_total, board_copy, player)
        board_copy = board.clone()
    ultimate_move = get_best_move(board_copy, scores_total)
    return ultimate_move


#board1 = provided.TTTBoard(3)

#for trial in range(50):
#    board2 = board1.clone()
#    mc_trial(board2, player_test)
#    print board2
#    mc_update_scores(scores_test, board2, player_test)
#    print scores_test[0],'\n', scores_test[1], '\n', scores_test[2], '\n'

#boardn = provided.TTTBoard(3)
#boardn.move(0,0,provided.PLAYERX)
#boardn.move(0,1,provided.PLAYERX)
#boardn.move(0,2,provided.PLAYERO)
#boardn.move(1,0,provided.PLAYERO)
#boardn.move(1,1,provided.PLAYERX)
#boardn.move(1,2,provided.PLAYERX)
#boardn.move(2,0,provided.PLAYERO)
#boardn.move(2,1,provided.PLAYERX)
#boardn.move(2,2,provided.PLAYERO)
#print boardn

#print mc_move(boardn, provided.PLAYERX, NTRIALS)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
