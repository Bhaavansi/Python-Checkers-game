### YOUR SOLUTION HERE
class CheckersGame () :
    def __init__ (self) :
        self.board = [
            [0,2,0,2,0,2,0,2],
            [2,0,2,0,2,0,2,0],
            [0,2,0,2,0,2,0,2],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1],
            [1,0,1,0,1,0,1,0],
        ]
        
        self.whoseMove = "white"
        self.isWon = False
    
    def checkWinner(self) :
        whitePieces = 0
        redPieces = 0
        for row in self.board:
            for column in row:
                if column == 1 or column == 3:
                    whitePieces+= 1
                if column == 2 or column == 4:
                    redPieces += 1
        
        if whitePieces == 0 and redPieces > 0:
            self.isWon = "red"
        elif whitePieces > 0 and redPieces == 0:
            self.isWon = "white"
        
    
    def changeTurn(self) :
        if self.whoseMove == "white":
            self.whoseMove = "red"
        else:
            self.whoseMove = "white"
    
    def parseMove (self, move) :
        validCoords = "01234567"
        listOfMoves = move.split(" ")
        listOfCoords = []
        if len(listOfMoves) < 2:
            raise ValueError
        for moves in listOfMoves:
            if len(moves) != 2:
                raise ValueError
            
            if moves[0] not in validCoords or moves[1] not in validCoords:
                raise ValueError
            
            listOfCoords.append((int(moves[0]),int(moves[1])))
        
        return tuple(listOfCoords)
            
    def move(self, move) :
        moves = self.parseMove(move)
        
        for i in range(len(moves) - 1):
            y = moves[i][0]
            x = moves[i][1]
            
            yTo = moves[i+1][0]
            xTo = moves[i+1][1]
            
            piece = self.board[y][x]
            self.board[y][x] = 0
            
            
            dy = yTo - y
            dx = xTo - x
            #capturing pieces
            if piece % 2 == 0 or (dy > 1): #if piece is red or moving down the board (increasing y)
                if dy > 1:
                    if dx < 0: 
                        self.board[yTo - 1][xTo + 1] = 0
                    else:
                        self.board[yTo - 1][xTo - 1] = 0
            elif piece % 2 != 0 or (dy < 1): # if piece is white or moving up the board (decreasing y)
                if dy < 1:
                    if dx < 0: 
                        self.board[y - 1][xTo + 1] = 0
                    else:
                        self.board[y - 1][xTo - 1] = 0
            
            #actually moving the piece and checking if a checker reaches the end of the board (kings)
            if piece == 1 and yTo == 0:
                self.board[yTo][xTo] = 3
                break
            elif piece == 2 and yTo == 7:
                self.board[yTo][xTo] = 4
                break
            else:
                self.board[yTo][xTo] = piece
            
            self.checkWinner()
            if self.isWon != False:
                break
        self.changeTurn()
        
    def isValidMove(self, move) : 
        if self.isWon != False:
            return False
        
        try: 
            moves = self.parseMove(move)
        except ValueError:
            return False
        
        
        for i in range(len(moves) - 1):
            y = moves[i][0]
            x = moves[i][1]
            
            yTo = moves[i+1][0]
            xTo = moves[i+1][1]
            piece = self.board[y][x]
            
            if piece == 0: # checks if it's a valid piece to move
                return False
            
            if self.board[yTo][xTo] != 0: # checks if the square is going to isn't occupied
                return False
            
            if self.whoseMove == "white" and (piece % 2 == 0): # checks if the wrong person is moving
                return False
            
            if self.whoseMove == "red" and (piece % 2 != 0): # checks if the wrong perosn is moving
                return False
            
            absdy = abs(yTo - y)
            absdx = abs(xTo - x)
            dy = yTo - y
            dx = xTo - x
            
            if (absdy == 1 and absdx == 1) or (absdy == 2 and absdx == 2): #ensures diagonal movement
                if self.whoseMove == "white" and piece == 1:
                    if dy > 0:
                        return False
                elif self.whoseMove == "red" and piece == 2:
                    if dy < 0:
                        return False
            else:
                return False
            
        return True

### EVERYTHING PAST THIS POINT IS A GIFT: Don't touch until December 25th        
    def __str__ (self) :
        out = "  0 1 2 3 4 5 6 7 \n  ╔═╤═╤═╤═╤═╤═╤═╤═╗\n"
        i = 0
        for row in self.board :
            out += f"{str(i)}║"
            j = 0
            for item in row :
                if item == 0:
                    out += "░" if (i + j) % 2 == 0 else " "
                elif item >= 1 and item <= 4:
                    out += ["○", "●", "♔", "♚"][item-1]
                out += "│"
                j += 1
            out = out[:-1]
            out += f"║{str(i)}\n ╟─┼─┼─┼─┼─┼─┼─┼─╢\n"
            i += 1
        out = out[:-18]
        out += "╚═╧═╧═╧═╧═╧═╧═╧═╝\n  0 1 2 3 4 5 6 7 \n"
        return out
    
def runGame (init = False, moveList = False) :
    game = CheckersGame()

    if (init != False) :
        game.board = init
    
    print("Checkers Initialized...")
    print(game)
    if (moveList != False) :
        print("Move List Detected, executing moves")
        for move in moveList :
            print(f"{game.whoseMove} makes move {move}\n")
            if (move == "q") :
                return
            if (game.isValidMove(move)) :
                game.move(move)
                print(game)
                if (game.isWon != 0) :
                    break
            else :
                print("Invalid Move")    
                
    print("Moves must be typed as coordinates (with no commas or brackets) separated by spaces. Row, then column.")
    print("Example: 54 43")
    print("When performing multiple jumps, enter each co-ordinate your piece will land on in sequence.")
    while (game.isWon == False) :
        print(f"{game.whoseMove} to move")
        move = input(">> ")
        if (move == "q") :
            return
        if (game.isValidMove(move)) :
            game.move(move)
            print(game)
            if (game.isWon != 0) :
                break
        else :
            print("Invalid Move")
    print("The Game is Finished!")
    print(f"Congratulations, {game.isWon}!")

