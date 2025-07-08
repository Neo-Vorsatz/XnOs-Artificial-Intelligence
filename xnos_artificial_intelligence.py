# Artificial Intelligence for the classic game "X and Os" or "Naughts and Crosses"
# Neo Vorsatz
# Last updated: 8 July 2025

from random import randint

#note to self: make AI learn to forget moves, regardless of which symbol it's playing with

class XnOs_AI():
    """
    Artificial Intelligence that starts with all possible moves, but rules out moves that result in failure
    """
    #characters
    BLANK = "."
    O = "O"
    X = "X"
    DRAW = "-"

    def __init__(self):
        #memory of the previous moves
        self.prev_move = None

        #generate all board state and valid moves, which assume this AI is playing as O
        self.moves = []
        self.inverted_boards = [] #list of board states that are the opposite/inverse of its index
        for i in range(3**9): #for every possible board state
            #create a string of rows
            board_state = self.board_state_int_to_str(i)
            string = ""
            for row in board_state.split("\n"):
                string += row
            
            #getting the inverted board state
            inv_board_state = ""
            for char in board_state:
                if char=="O":
                    inv_board_state += "X"
                elif char=="X":
                    inv_board_state += "O"
                else:
                    inv_board_state += char
            self.inverted_boards.append(self.board_state_str_to_int(inv_board_state))
            
            #count Os and Xs
            num_Os = 0
            num_Xs = 0
            for square in string:
                if square==XnOs_AI.O:
                    num_Os += 1
                if square==XnOs_AI.X:
                    num_Xs += 1
            
            #checking if it's valid to make a move
            difference = num_Os-num_Xs
            if difference>1: #if there are too many Os
                self.moves.append(None)
                continue
            if difference<-1: #if there are too many Xs'
                self.moves.append(None)
                continue
            if difference==1: #if its definitely X's turn to play
                self.moves.append(None)
                continue
            if self.game_state(board_state=i)!=XnOs_AI.BLANK: #if the game ends in this state
                self.moves.append(None)
                continue

            #add empty list of possible moves
            self.moves.append([])

            #find all possible moves
            for square in range(9): #for every square on the board
                if string[square]==XnOs_AI.BLANK: #if this square is empty
                    self.moves[i].append(i+3**square) #add the new board state with this move played

    def board_state_str_to_int(self, board_state:str) -> int:
        """
        Converts a board state represented with a string into an integer, using base-three
        """
        #dictionary to convert the symbols
        conversion = {XnOs_AI.BLANK:0, XnOs_AI.O:1, XnOs_AI.X:2}

        #generating a string of the symbols
        string = ""
        for row in board_state.split("\n"):
            string += row

        #converting the string of symbols into a whole number
        value = 0
        power = 0
        for symbol in string:
            value += conversion[symbol]*(3**power)
            power += 1
        
        #returning integer representation
        return value
    
    def board_state_int_to_str(self, board_state:int) -> int:
        """
        Converts a board state represented with an int into a string, using base-three
        """
        #list to convert the integers
        conversion = [XnOs_AI.BLANK, XnOs_AI.O, XnOs_AI.X]

        #convert the int into a base-three list
        digits = []
        for power in range(9):
            digits.append((board_state//3**power)%3) #div gets the amount of that power, and modulo remove higher powers
        
        #generating a string representation
        string = ""
        for i in range(9):
            if digits[i] in range(3): #if the digit is in a valid index
                string += conversion[digits[i]]
            else:
                string += XnOs_AI.BLANK
            if (i+1)%3==0: #if this was the last symbol in the row
                string += "\n"
        
        #returning string representation
        return string
    
    def has_pattern(self, board_state:int, pattern:int) -> bool:
        """
        Checks if a pattern exists in the board. This is position-sensitive
        """
        board_state = self.board_state_int_to_str(board_state=board_state)
        pattern = self.board_state_int_to_str(board_state=pattern)
        for i in range(12): #12 iterations, because there are new-line characters
            if pattern[i]!=XnOs_AI.BLANK and pattern[i]!=board_state[i]: #if this is not a blank space, and the symbols don't match
                return False
        return True

    def game_state(self, board_state:int|str) -> str:
        """
        Returns 'O' if O won, 'X' if X won, '.' if the game is incomplete, '-' if it's a draw
        """
        #convert the board state to an integer
        if isinstance(board_state, str):
            board_state = self.board_state_str_to_int(board_state=board_state)
        
        #check winning rows
        for i in range(3):
            pattern = (1+3+9)*(27**i) #row completed by O
            if self.has_pattern(board_state=board_state, pattern=pattern):
                return XnOs_AI.O
            if self.has_pattern(board_state=board_state, pattern=2*pattern):
                return XnOs_AI.X
        
        #check winning
        for i in range(3):
            pattern = (1+27+729)*(3**i) #column completed by O
            if self.has_pattern(board_state=board_state, pattern=pattern):
                return XnOs_AI.O
            if self.has_pattern(board_state=board_state, pattern=2*pattern):
                return XnOs_AI.X
        
        #check winning diagonals
        pattern = 1+81+6561 #top-left diagonal
        if self.has_pattern(board_state=board_state, pattern=pattern):
            return XnOs_AI.O
        if self.has_pattern(board_state=board_state, pattern=2*pattern):
            return XnOs_AI.X
        pattern = 9+81+729 #top-right diagonal
        if self.has_pattern(board_state=board_state, pattern=pattern):
            return XnOs_AI.O
        if self.has_pattern(board_state=board_state, pattern=2*pattern):
            return XnOs_AI.X
        
        #checking if there are empty squares
        for symbol in self.board_state_int_to_str(board_state=board_state):
            if symbol==XnOs_AI.BLANK:
                return XnOs_AI.BLANK
        
        #the game ended in a draw
        return XnOs_AI.DRAW
    
    def start_game(self, symbol:str=None) -> str:
        """
        Notes which symbol belongs to the AI,
        and clears the AI's memory of the past few moves.
        Returns an empty board
        """
        if symbol in [XnOs_AI.O, XnOs_AI.X]: #if a valid symbol was given
            self.symbol = symbol
        else:
            self.symbol = XnOs_AI.O
        self.prev_move = None

        return self.board_state_int_to_str(board_state=0) #retun an empty board
    
    def move(self, board_state:str) -> str:
        """
        Takes a board state,
        makes a move,
        records the move,
        then returns the new board state
        """
        #check if no board state was received
        if board_state==None:
            return None
        
        #get the number corresponding to the board state
        board_num = self.board_state_str_to_int(board_state=board_state)

        #inverting the board if the AI is playing as X
        if self.symbol=="X":
            board_num = self.inverted_boards[board_num]

        #check the game state
        game_state = self.game_state(board_state=board_num)
        if game_state==XnOs_AI.X: #if the AI lost
            #forget moves
            bad_moves = [self.prev_move] #list of bad moves that need to be removed
            while len(bad_moves)>0: #for every bad move
                state_str = self.board_state_int_to_str(board_state=bad_moves[0])
                for i in range(len(state_str)): #for each character in the state_str
                    if state_str[i]==XnOs_AI.O:
                        #generate a possible prior state
                        prev_bad_str = list(state_str)
                        prev_bad_str[i] = XnOs_AI.BLANK
                        prev_bad_str = "".join(prev_bad_str)
                        prev_bad_state = self.board_state_str_to_int(board_state=prev_bad_str)
                        if self.moves[prev_bad_state]!=None:
                            if bad_moves[0] in self.moves[prev_bad_state]: #if the first bad move exists in this board state
                                self.moves[prev_bad_state].remove(bad_moves[0]) #remove the move
                                if len(self.moves[prev_bad_state])==0: #if there are no more ways to respond to this board state
                                    #any move that allows the opponent to lead to this state is also a faulty state
                                    for j in range(len(prev_bad_str)):
                                        if prev_bad_str[j]==XnOs_AI.X:
                                            #generate a bad previous move
                                            prev_str = list(prev_bad_str)
                                            prev_str[j] = XnOs_AI.BLANK
                                            prev_str = "".join(prev_str)
                                            prev_bad_move = self.board_state_str_to_int(board_state=prev_str)
                                            bad_moves.append(prev_bad_move) #note the earlier move as a bad move, since it lead to not viable moves
                bad_moves.pop(0) #remove the move
        if game_state!=XnOs_AI.BLANK: #if the game has ended
            self.prev_move = None
            return None

        #check validity
        if len(self.moves[board_num])==0: #if the AI doesn't know any moves to respond with
            #this code theoretically shouldn't be reached in a proper game
            return None
        
        #choose a move and record it
        possible_moves = self.moves[board_num]
        new_board_num = possible_moves[randint(0, len(possible_moves)-1)]
        self.prev_move = new_board_num #record the previous move
    
        #check the game state again
        game_state = self.game_state(board_state=new_board_num)
        if game_state!=XnOs_AI.BLANK: #if the game has ended
            self.prev_moves = []

        #inverting the board if the AI is playing as X
        if self.symbol=="X":
            new_board_num = self.inverted_boards[new_board_num]
        
        #return the new board state
        return self.board_state_int_to_str(board_state=new_board_num)

if __name__=="__main__":
    SETS = 10
    GAMES_IN_SET = 1000

    #function to make two AIs play a single game
    def play_game(player:str, print_game:bool=False) -> str:
        player_O.start_game(symbol=XnOs_AI.O)
        new_board = player_X.start_game(symbol=XnOs_AI.X)

        while new_board!=None: #while the game hasn't ended
            board = new_board
            if player==XnOs_AI.O:
                player = XnOs_AI.X
                new_board = player_O.move(board_state=board)
            else:
                player = XnOs_AI.O
                new_board = player_X.move(board_state=board)
            if print_game and new_board!=None:
                print(new_board+"====")
        return player_O.game_state(board_state=board)
                
    #initialise players
    player_O = XnOs_AI()
    player_X = XnOs_AI()

    #play multiple sets of games, demonstrating the results of each set
    for i in range(SETS): #for each set
        #initialise counting variables
        X_wins = 0
        O_wins = 0
        draws = 0
        def update_scores(game_result:str):
            global X_wins
            global O_wins
            global draws
            if game_result==XnOs_AI.X:
                X_wins += 1
            elif game_result==XnOs_AI.O:
                O_wins += 1
            elif game_result==XnOs_AI.DRAW:
                draws += 1
            else:
                print(game_result)

        #first game for demonstration
        print("Demonstration after", GAMES_IN_SET*i, "games:")
        result = play_game(player=XnOs_AI.X, print_game=True) #play a demonstation game
        update_scores(result)

        #last games
        for j in range(GAMES_IN_SET-1):
            result = play_game(player=XnOs_AI.X)
            update_scores(result)

        #results
        print("Outcome from past", GAMES_IN_SET, "games:")
        print("X Wins:", X_wins, "| O Wins:", O_wins, "| Draws:", draws)