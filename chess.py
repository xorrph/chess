#TO DO:
#MAKE IT DO THE CHECKING ON THE PLAYERS TURN
#ONLY CHECK PLAYER COLOUR PIECES

class board():
    def __init__(self):
        self.board = []
        self.pM = [[],[]]#contains two lists for possible white moves and possible black moves, access using the p value
        self.empty = "   "

    def makeBoard(self,width,length): 
      for i in range(length):
         self.board.append([self.empty] * width)
      self.initPieces()

    def initPieces(self):
        for i in range(len(self.board)):
            self.board[1][i] = Pawn(1,i,"b")
            self.board[6][i] = Pawn(6,i,"w")
            if i ==0:
                self.board[0][i] = Rook(0,i,"b")
                self.board[7][i] = Rook(7,i,"w")
            elif i ==1:
                 self.board[0][i] = Knight(0,i,"b")
                 self.board[7][i] = Knight(7,i,"w")
            elif i ==2:
                 self.board[0][i] = Bishop(0,i,"b")
                 self.board[7][i] = Bishop(7,i,"w")
            elif i ==3:
                 self.board[0][i] = Queen(0,i,"b")
                 self.board[7][i] = Queen(7,i,"w")
            elif i ==4:
                 self.board[0][i] = King(0,i,"b")
                 self.board[7][i] = King(7,i,"w")
            elif i == 5:
                 self.board[0][i] = Bishop(0,i,"b")
                 self.board[7][i] = Bishop(7,i,"w")
            elif i ==6:
                 self.board[0][i] = Knight(0,i,"b")
                 self.board[7][i] = Knight(7,i,"w")
            elif i ==7:
                 self.board[0][i] = Rook(0,i,"b")
                 self.board[7][i] = Rook(7,i,"w")
                

    def displaySingleBoard(self,user):
        count = 8
        space = "     "
        print("{}'s board: ".format(user))
        w = (space + "A" + space +"B" + space + "C" + space + "D" + space + "E" + space + "F" + space + "G" + space + "H")
        b = (space + "H" + space +"G" + space + "F" + space + "E" + space + "D" + space + "C" + space + "B" + space + "A")
        if user == "w":
            print(w)
            count = 8
        else:
            print(b)
            count = -1
        for row in self.board:
            sRow = []
            for piece in row:
                if piece != self.empty:
                    sRow.append(piece.sym)
                else:
                    sRow.append(self.empty)
            grid = (" | ").join(sRow)
            print("  +" + ("-----+" * 8))
            print(str(abs(count)) + (" | ") + grid + (" | "))
            count -= 1
        print("  +" + ("-----+" * 8))

    def updatePos(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != self.empty:
                    self.board[i][j].ypos = i
                    self.board[i][j].xpos = j
                    if self.board[i][j].sym == " Q ":
                        self.board[i][j].r.ypos = i
                        self.board[i][j].r.xpos = j
                        self.board[i][j].b.ypos = i
                        self.board[i][j].b.xpos = j

    def updateVis(self,players,p):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != self.empty:
                    if self.board[i][j].sym == " Q " or self.board[i][j].sym == " K ":
                        self.board[i][j].posMoves(self,self.board,players,p)
                        self.pM[0] = list(dict.fromkeys(self.pM[0]))
                        self.pM[1] = list(dict.fromkeys(self.pM[1]))
                        
        
    def flipBoard(self):
        print("########################################################")
        for x in range(4):
            for y in range(8):
                self.board[7-y][7-x],self.board[y][x] = self.board[7-y][7-x],self.board[y][x]
                self.board[y][x],self.board[7-y][7-x] = self.board[7-y][7-x], self.board[y][x]
        self.updatePos()


# Define a base class for a chess piece
class ChessPiece:
    def __init__(self,ypos,xpos,colour):
        self.xpos = xpos #pieces position
        self.ypos = ypos
        self.colour = colour #team
        self.sym = "" # print symbol

    def move(self, y,x,bd):
        print(y,x)
        print(self.ypos,self.xpos)
        print(bd[y][x],bd[self.ypos][self.xpos])
        temp = bd[self.ypos][self.xpos]
        bd[self.ypos][self.xpos]= "   "
        bd[y][x] = temp
        self.ypos = y
        self.xpos = x

    def preCheck(self, new_position,currentN,players,p,bd,b):
        bd = b.board
        result = wb(players[p].colour,new_position)
        if new_position == currentN:
            return False
        if players[p].colour != bd[self.ypos][self.xpos].colour:
            return False
        if result:
            y, x = result
            temp = listCopy(bd)
            if self.enPassant(y,x,bd):
                self.move(y,x,bd)
                return True
            if bd[self.ypos][self.xpos].sym == " K ":#if its a king pass in extra parameters
                result2 = self.checkMove(y,x,bd,b,players,p)
            else:
                result2 = self.checkMove(y,x,bd)
            b.updatePos()
            b.updateVis(players,p)
            if players[p].check:  # If the king is in check
                b.pM =[[],[]]
                b.board = listCopy(temp)  # Revert to the original board
                bd = listCopy(temp)  # Ensure bd matches the original state
                b.updateVis(players, p)  # Recalculate visibility
                players[p].check = False  # Reset check flag
                return False 
            if result2:
                b.board = bd
                b.updateVis(players, p)
                print(result2, " moves from " + currentN + " to " + new_position)
                return True
            else:
                return False
        else:
            return False

        
        
    def enPassant(self,y,x,bd):
        if y + 1 <= 7:
          if bd[y + 1][x] !=  "   ":
              if bd[y + 1][x].sym == " P " and bd[y + 1][x].two and bd[y+1][x] != bd[self.ypos][self.xpos]:
                  bd[y + 1][x] =  "   "
                  return True
        return False


    def checkMove(self, new_position,bd):
        raise NotImplementedError("This method should be overridden by subclasses")

    def posMoves(self,b,bd,players,p):
        raise NotImplementedError("This method should be overridden by subclasses")

    def __repr__(self):
        return self.sym

# Define specific classes for each type of piece
class Pawn(ChessPiece):
    def __init__(self,xpos,ypos,colour):
        super().__init__(xpos,ypos,colour)
        self.sym = " P "
        self.first = True
        self.two = False        
    def checkMove(self, y,x,bd,c = False):
        if self.two:
            self.two = False
        if bd[y][x] != "   " and not c:
                if bd[y][x].colour ==bd[self.ypos][self.xpos].colour :
                    return False
        if bd[self.ypos-1][self.xpos] ==  "   " or bd[self.ypos-2][self.xpos] ==  "   ": # make sure nothing is blocking pawn movement
            if bd[y+2][x] == bd[self.ypos ][self.xpos] and self.first == True: #checks if the new position 2 spaces back is the pawn and if its the first time using this pawn
                if not c:
                    self.first = False
                    self.two = True
                return self.promote(y,x,bd,c)
            elif bd[y+1][x] == bd[self.ypos ][self.xpos]: #checks if the new position 1 space back is the pawn
                if self.first == True and not c:
                    self.first = False
                return self.promote(y,x,bd,c)
        if self.ypos - y ==1 and abs(self.xpos-x) == 1:
            if bd[y][x] != "   ":
                if  bd[y][x].colour !=bd[self.ypos][self.xpos].colour :
                    return self.promote(y,x,bd,c)
        return False
            
    def promote(self,y,x,bd,c):
        if not c:
            self.move(y,x,bd)
        if self.ypos == 0:
            pChoice = input("Enter what you want to promote to(N, B, R, anything else for Q): ")
            if pChoice.upper().strip() == "N":
                bd[self.ypos][self.xpos] = Knight(self.xpos,self.ypos,self.colour)
            elif pChoice.upper().strip() == "B":
                bd[self.ypos][self.xpos] = Bishop(self.xpos,self.ypos,self.colour)
            elif pChoice.upper().strip() == "R":
                bd[self.ypos][self.xpos] = Rook(self.xpos,self.ypos,self.colour)
            else:
                bd[self.ypos][self.xpos] = Queen(self.xpos,self.ypos,self.colour)
        return "Pawn"

    def posMoves(self, b,bd,players,p):
        #crashes because checkMove is only made for checking of current player
        #maybe use flipboard? and c?
        pMoves = [(self.ypos -1,self.xpos-1),((self.ypos -1,self.xpos+1)),(self.ypos -1,self.xpos),(self.ypos -2,self.xpos)]
        if bd[self.ypos][self.xpos].colour == players[p].colour:
            for m in pMoves:
                if m[0] < 0 or m[0] > 7 or m[1] < 0 or m[1] > 7:
                    continue
                if self.checkMove(m[0],m[1],bd,True):
                    b.pM[p].append(m)

class Knight(ChessPiece):
    def __init__(self,xpos,ypos,colour):
        super().__init__(xpos,ypos,colour)
        self.sym = " N "
        
    def checkMove(self, y,x,bd,c = False):
        if y-self.ypos == 0 or x-self.xpos == 0: return False #div error
        if abs(((y-self.ypos)**2) +((x-self.xpos)**2)) == 5:
            print("knight pass")#uses gradient formula to check if its a 2 or 0.5 since knights will always move with +- 2 and +-1 in any direction
            if bd[y][x]!= "   ":# checks if a piece is there
                if bd[y][x].colour == bd[self.ypos][self.xpos].colour: return False # check if its your piece is blocking
            if not c:
                self.move(y,x,bd)#when pass checks, it then moves
            return "Knight"# move output
        
    def posMoves(self, b,bd,players,p):
        # Possible changes
        changes = [1, -1, 2, -2]
        kMoves =  [(self.ypos + dy, self.xpos + dx) for dy in changes for dx in changes]
        for m in kMoves:
            if m[0] < 0 or m[0] > 7 or m[1] < 0 or m[1] > 7:
                continue
            if self.colour != players[p].colour: continue
            if self.checkMove(m[0],m[1],bd,True):
                b.pM[p].append(m)

class Bishop(ChessPiece):
    def __init__(self,xpos,ypos,colour):
        super().__init__(xpos,ypos,colour)
        self.sym = " B "
        
    def checkMove(self, y,x,bd,c = False):
        if abs(y-self.ypos) == abs(x - self.xpos): #check if absolute of difference in y is same as absolute of difference in x
            yd = int((y-self.ypos)/abs(y-self.ypos))#set y direction
            xd =  int((x-self.xpos)/abs(x-self.xpos))# set x direction
            j = self.xpos + xd #start 1 ahead in the x direction (so the check doesnt pick the wrong object
            for i in range(self.ypos+yd,y+yd,yd):#same start as x, to end y + the direction becuase of python exclusion, and the step directoin 
                     if bd[i][j] != "   ": # check if it not empty
                                if  bd[i][j].colour ==bd[self.ypos][self.xpos].colour or (i != y and j!= x): # check if it is your piece or opponent piece blocking you
                                    return False # return False (invalid move)
                                else:
                                    break #stop here
                     j = j + xd # add to the incrementing x axis
            if not c:
                self.move(y,x,bd) # once out of loop (destination without any blocking pieces)
            return "Bishop" # confirmation message
        return False
            

    def posMoves(self,b,bd,players,p):
        print("bishoppos",self.ypos,self.xpos)
        yd = int(((7-self.ypos)-self.ypos)/abs((7-self.ypos)-self.ypos))#set y direction furthest away
        xd = int(((7-self.xpos)-self.xpos)/abs((7-self.xpos)-self.xpos))#set x direction furthest away
        j = self.xpos + xd #start 1 ahead in the x direction (so the check doesnt pick the wrong object
        dones = [False,False,False,False]
        count = 1
        for i in range(self.ypos+yd,(7-self.ypos)+yd,yd):#same start as x, to end y + the direction becuase of python exclusion, and the step directoin 
                 
                 dones[0] = self.checkPosM(b,bd,i,j,dones[0],players,p)
                 dones[1] = self.checkPosM(b,bd,i+((-2*count)*(yd)),j,dones[1],players,p)
                 dones[2] = self.checkPosM(b,bd,i+((-2*count)*(yd)),j+((-2*count)*(xd)),dones[2],players,p)
                 dones[3] = self.checkPosM(b,bd,i,j+((-2*count)*(xd)),dones[3],players,p)
                 j = j + xd # add to the incrementing x axis
                 count +=1 
                 
    def checkPosM(self,b,bd,i,j,done,players,p):
        if done: return True
        if i < 0 or j < 0: return True
        if i > 7 or j > 7: return True
        if (i,j) == (self.ypos,self.xpos): return True
        if self.colour != players[p].colour: return True
        if self.checkMove(i,j, bd,True):
            b.pM[p].append((i,j))
            return False
        else:
            return True
        

class Rook(ChessPiece):
    def __init__(self,xpos,ypos,colour):
        super().__init__(xpos,ypos,colour)
        self.sym = " R "
        
    def checkMove(self, y,x,bd,c = False): #add can take opposite peices but can not go over any pieces
            if y - self.ypos == 0 or x - self.xpos == 0:
                if x !=self.xpos :
                    d = int((x-self.xpos)/abs(x-self.xpos))
                    for i in range(self.xpos+d,x+d,d):
                        if bd[y][i] != "   ":
                            if  bd[y][i].colour ==bd[self.ypos][self.xpos].colour or (i != x):
                                return False
                            else:
                                break
                elif y !=self.ypos :
                    d = int((y-self.ypos)/abs(y-self.ypos))
                    for i in range(self.ypos+d,y+d,d):
                        if bd[i][x] != "   ":
                            if  bd[i][x].colour ==bd[self.ypos][self.xpos].colour or (i != y):
                                return False
                            else:
                                break
                if not c:
                    self.move(y,x,bd)
                return "Rook"

    def posMoves(self,b,bd,players,p):
        rMoves = []
        for i in range(8):
            rMoves.append((self.ypos + i,self.xpos))
            rMoves.append((self.ypos - i,self.xpos))
            rMoves.append((self.ypos,self.xpos + i))
            rMoves.append((self.ypos,self.xpos - i))
        for move in rMoves:
            if move[0] < 0 or move[1] < 0: continue
            if move[0] > 7 or move[1] > 7: continue
            if move == (self.ypos,self.xpos): continue
            if self.colour != players[p].colour: continue
            if self.checkMove(move[0],move[1], bd,True):b.pM[p].append((move))
            
        

class Queen(ChessPiece):
    def __init__(self,xpos,ypos,colour):
        super().__init__(xpos,ypos,colour)
        self.sym = " Q "
        self.r = Rook(self.ypos,self.xpos,self.colour)
        self.b = Bishop(self.ypos,self.xpos,self.colour)
        
    def checkMove(self, y,x,bd):
        if self.r.checkMove(y,x,bd):
            self.ypos,self.xpos = self.r.ypos,self.r.xpos
            self.b.ypos,self.b.xpos = self.r.ypos,self.r.xpos
            return "Queen"
        if self.b.checkMove(y,x,bd):
            self.ypos,self.xpos = self.b.ypos,self.b.xpos
            self.r.ypos,self.r.xpos = self.b.ypos,self.b.xpos
            return "Queen"
        
        
    def posMoves(self,b,bd,players,p):
        self.r.posMoves(b,bd,players,p)
        self.b.posMoves(b,bd,players,p)
           
        

class King(ChessPiece):
    def __init__(self,xpos,ypos,colour):
        super().__init__(xpos,ypos,colour)
        self.sym = " K "
        self.check = False
        
    def checkMove(self, y,x,bd,b,players,p):
        if(7-self.xpos,7-self.ypos) in b.pM[p]:
            print("Your King is in check")
            players[p].check = True
            self.check = True
            return False
        if abs(y - self.ypos) == 1 or abs(x - self.xpos) == 1:
            if (y,x) in b.pM[1-p]:
                print("Your King is blocked")
                return False
            self.move(y,x,bd)
            return "King"
        return False
    
    def posMoves(self,b,bd,players,p):
        print((7-self.xpos,7-self.ypos))
        if(7-self.xpos,7-self.ypos) in b.pM[1-p]:
            players[p].check = True
            self.check = True




class player():
    def __init__(self,colour):
        self.colour = colour
        self.points = 0
        self.check = False

    

def convW(notation):
    letters = {
            "a" : 0,
            "b" : 1,
            "c" : 2,
            "d" : 3,
            "e" : 4,
            "f" : 5,
            "g" : 6,
            "h" : 7
        }
    if notation[0] in letters and 8 -int(notation[1]) < 8:
        xAxis = letters[notation[0].lower().strip()]
        yAxis = 8 - int(notation[1])
        return yAxis, xAxis
    else:
        return False

def convB(notation):
    letters = {
            "h" : 0,
            "g" : 1,
            "f" : 2,
            "e" : 3,
            "d" : 4,
            "c" : 5,
            "b" : 6,
            "a" : 7
        }
    if notation[0] in letters and 8 -int(notation[1]) < 8:
        xAxis = letters[notation[0].lower().strip()]
        yAxis = int(notation[1]) - 1
        return yAxis, xAxis
    else:
        return False



def wb(p,newpos):
    if p == "w":
            result = convW(newpos)# x and  y = new x and y from the conversion function (converts chess coords to array coords)
    else:
            result = convB(newpos)
    return result

def listCopy(list1):
    out = []
    for x in range(len(list1)):
        temp = []
        for elem in list1[x]:
            temp.append(elem)
        out.append(temp)
    return out





b = board()
b.makeBoard(8,8)
bd = b.board
players = (player("w"),player("b"))
kings = (bd[7][4],bd[0][4])
checks = (kings[0].check,kings[1].check)
p = 0
while True not in checks:
    b.displaySingleBoard(players[p].colour)
    m = input("Enter a move in the format 'm0m1': ")
    oY, oX = wb(players[p].colour,m[:2])
    print("wop",oY,oX)
    if not p:#when w turn
        b.pM = [[],[]]
    while not (bd[oY][oX].preCheck( m[2:],m[:2],players, p,bd,b)):
        #bd = b.board
        m = input("Invalid move, enter a move in the format 'm0m1': ")
        oY, oX = wb(players[p].colour,m[:2])
    b.updateVis(players,p)
    b.displaySingleBoard(players[p].colour)
    b.flipBoard()
    p = 1 - p
    if bd[oY][oX] != b.empty:
        if bd[oY][oX].sym == " P " and p == 1: bd[oY][oX].two = False #after blacks turn en passant is no longer valid
    #b.updateVis(players,p)#REMEMBER TO CLEAR PM FOR WHITE
    print(p)
input()



# max(0, x - 1), min(width, x + 2)):
# max(0, y - 1), min(height, y + 2)
# use min and max for out of bounds

##        if abs(y-x) == abs(self.ypos - self.xpos):
##            self.move(y,x,bd)
##        else:
##            return False

