# Grupo 104:
# 99405 Clara Pereira 
# 99432 Marta Sereno

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id



#--------------------------------------------------------------------------------------------------------------



class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, row, col, hints, boats, mboard):

        dim = len(row) 
        self.dim = dim #dimensão do tabuleiro dim x dim
        self.boats = boats #dicionário com a contagem dos barcos que falta colocar
        self.row = row #lista com a contagem das linhas - peças que falta preencher
        self.col = col #lista com a contagem das colunas - peças que falta preencher
        self.hints = hints #lista com hints
        self.mboard = mboard #matriz correspondente ao tabuleiro
    

    
    def fillwater_row(self, row: int):
        """Preenche a linha indicada com água nos espaços vazios"""
        board = self.mboard 
        dim = self.dim
        for i in range(dim):
            if board[row][i] == "":
                board[row][i] = "w"
        self.row[row] = -1 #indica que linha já está preenchida



    def fillwater_col(self, col: int):
        """Preenche a coluna indicada com água nos espaços vazios"""
        board = self.mboard 
        dim = self.dim
        for i in range(dim):
            if board[i][col] == "":
                board[i][col] = "w"
        self.col[col] = -1 #indica que coluna já está preenchida



    def values(self, info):
        """Devolve todos os valores adjacentes a um determinado barco"""
        item = info[0]
        coord = info[1]

        if item == "C" or item == "c":
            row = coord[0]
            col = coord[1]
            return [self.top_value(row, col), self.topright_value(row, col), self.right_value(row, col), self.bottomright_value(row, col), self.bottom_value(row, col), self.bottomleft_value(row, col), self.left_value(row, col), self.topleft_value(row, col)]
        
        elif item == "rboat":
            row = coord[0]
            cols = coord[1]
            return [self.top_value(row,col) for col in cols]  + self.right2(row, cols[-1])  + [self.bottom_value(row,col) for col in cols] + self.left2(row, cols[0])
        
        elif item == "cboat":
            rows = coord[0]
            col = coord[1]
            return self.top2(rows[0], col)  + [self.right_value(row,col) for row in rows] + self.bottom2(rows[-1], col) + [self.left_value(row,col) for row in rows]
       


    def surround(self, info):
        """Preenche os valores à volta do barco com água"""
        item = info[0]
        coord = info[1]
        board = self.mboard

        if item == "c" or item == "C":
            row = coord[0]
            col = coord[1]
            values = self.values(info)
            # lista das coordenadas dos valores adjacentes
            list = [(row-1, col), (row-1, col+1), (row, col+1), (row+1, col+1), (row+1, col), (row+1, col-1), (row, col-1), (row-1, col-1)]

            for i in range(len(values)):
                if values[i] != "Non-existant":
                    if values[i] == "":
                        board[list[i][0]][list[i][1]] = "w"

        elif item == "rboat":
            row = coord[0]
            cols = coord[1]
            left = cols[0]
            right = cols[-1]
            values = self.values(info)
            # lista das coordenadas dos valores adjacentes
            list = [(row-1,col) for col in cols] + [(row-1,right+1), (row, right+1), (row+1, right+1)] + [(row+1,col) for col in cols] +  [(row-1,left-1), (row, left-1), (row+1, left-1)]
            for i in range(len(values)):
               if values[i] != "Non-existant":
                    if values[i] == "":
                        board[list[i][0]][list[i][1]] = "w"

        elif item == "cboat":
            rows = coord[0]
            col = coord[1]
            top = rows[0]
            bottom = rows[-1]
            values = self.values(info)
            # lista das coordenadas dos valores adjacentes
            list = [(top-1,col-1), (top-1, col), (top-1, col+1)] + [(row,col+1) for row in rows] + [(bottom+1,col-1), (bottom+1, col), (bottom+1, col+1)] +  [(row,col-1) for row in rows] 
            for i in range(len(values)):
               if values[i] != "Non-existant":
                    if values[i] == "":
                        board[list[i][0]][list[i][1]] = "w"
            
              
        
    def fill(self, info:list):
        """Coloca o item na posiçao indicada, rodeia-o de água, atualiza o valor das contagens das rows e cols, atualiza boats"""
        item = info[0]
        coord = info[1]
        row = self.row
        col = self.col
        board = self.mboard 

        if item == "c" or item == "C":
            r = coord[0]
            c = coord[1]
            self.boats["1"] -= 1 #atualiza nº de barcos de 1 que falta preencher
            row[r] -= 1 #atualiza contagem das linhas
            col[c] -= 1 # atualiza contagem das colunas
            board[r][c] = item   
        
        elif item == "rboat":
            r = coord[0]
            cs = coord[1]
            size = len(cs)
            self.boats[str(size)] -= 1 #atualiza nº de barcos de comprimento = size que falta preencher
            row[r] -= size #atualiza contagem da linha
            
            if board[r][cs[0]] == "":
                board[r][cs[0]] = "l"
                
            if board[r][cs[-1]] == "":
                board[r][cs[-1]] = "r"

            for c in cs :
                col[c] -= 1 #atualiza contagem da coluna por cada peça colocada
                if board[r][c] == "":
                    board[r][c] = "m"
                    
        elif item == "cboat": 
            rs = coord[0]
            c = coord[1]
            size = len(rs)
            self.boats[str(size)] -= 1  #atualiza nº de barcos de comprimento = size que falta preencher
            col[c] -= size #atualiza contagem da coluna

            if board[rs[0]][c] == "":
                board[rs[0]][c] = "t"
                
            if board[rs[-1]][c] == "":
                board[rs[-1]][c] = "b"
                
            for r in rs : 
                row[r] -= 1 #atualiza contagem da linha por cada peça colocada
                if board[r][c] == "":
                    board[r][c] = "m"
                        
        self.surround(info) #rodeia de água 
        


    """Valores raio 1"""
 
    def right_value(self, row: int, col: int):
        """Devolve valor à direita"""
        if col >= self.dim-1:
            return "Non-existant"
        else:
            return self.mboard[row][col+1]
        
    def left_value(self, row: int, col: int):
        """Devolve valor à esquerda"""
        if col <= 0:
            return "Non-existant"
        else:
            return self.mboard[row][col-1]
        
    def top_value(self, row: int, col: int):
        """Devolve valor em cima"""
        if row <= 0:
            return "Non-existant"
        else:
            return self.mboard[row-1][col]
        
    def bottom_value(self, row: int, col: int):
        """Devolve valor em baixo"""
        if row >= self.dim-1:
            return "Non-existant"
        else:
            return self.mboard[row+1][col]
     
    def topleft_value(self, row: int, col: int):
        """Devolve valor no canto superior esquerdo"""
        if row <= 0 or col <= 0:
            return "Non-existant"
        else:
            return self.mboard[row-1][col-1]
        
    def topright_value(self, row: int, col: int):
        """Devolve valor no canto superior direito"""
        if row <= 0 or col >= self.dim-1:
            return "Non-existant"
        else:
            return self.mboard[row-1][col+1]
        
    
    def bottomleft_value(self, row: int, col: int):
        """Devolve valor no canto inferior esquerdo"""
        if row >= self.dim-1 or col <= 0:
            return "Non-existant"
        else:
            return self.mboard[row+1][col-1]
        

    def bottomright_value(self, row: int, col: int):
        """Devolve valor no canto inferior direito"""
        if row >= self.dim-1 or col >= self.dim-1:
            return "Non-existant"
        else:
            return self.mboard[row+1][col+1]
        


    """Valores raio 2"""

    def top2(self, row, col):
        """Devolve os três valores acima"""
        return [self.topleft_value(row,col), self.top_value(row,col), self.topright_value(row,col)]
        
    def right2(self, row, col):
        """Devolve os três valores à direita"""
        return [self.topright_value(row,col), self.right_value(row,col), self.bottomright_value(row,col)]
        
    def bottom2(self, row, col):
        """Devolve os três valores em baixo"""
        return [self.bottomleft_value(row,col), self.bottom_value(row,col), self.bottomright_value(row,col)]
        
    def left2(self, row, col):
        """Devolve os três valores à esquerda"""
        return [self.topleft_value(row,col), self.left_value(row,col), self.bottomleft_value(row,col)]
    
    

    def canput(self, info):
        """Devolve True se for possível colocar um barco, devolve False caso contrário"""
        item = info[0]
        coord = info[1]
        board = self.mboard
        boats = self.boats
        dim= self.dim
        ROW = self.row
        COL = self.col

        if item == "c" or item == "C":
            row = coord[0]
            col = coord[1]
            #verifica se cabe na contagem da linha e coluna e se a posição está vazia e se ainda pode pôr esse tamanho de barco
            if board[row][col] != "" or ROW[row]-1 < 0 or COL[col]-1 < 0 or boats["1"] == 0: 
                return False

            #raio 1
            for x in self.values(info): 
                if x not in ["w", "W", "", "Non-existant"]:
                    return False
                    
            #raio 2
            #linha de cima 
            above = self.top2(row-1,col)
            for x in above:
                if x == "T" or x == "t":
                    return False   
            #linha do lado direito 
            sider = self.right2(row,col+1)
            for x in sider:
                if x == "R" or x == "r":
                    return False    
            #linha de baixo 
            below = self.bottom2(row+1,col)
            for x in below:
                if x == "B" or x == "b":
                    return False  
            #linha do lado esquerdo 
            sidel = self.left2(row, col-1)
            for x in sidel:                    
                if x == "L" or x == "l":
                    return False
                    


        if item == "rboat":
            row = coord[0]
            cols = coord[1]
            boatdim=len(cols)
            left = cols[0]
            right = cols[-1]
            #verifica se cabe na contagem da linha e se as posições são válidas e se ainda pode pôr esse tamanho de barco
            if right >= dim or left < 0 or ROW[row] - boatdim < 0 or boats[str(boatdim)] == 0:
                return False
            
            #verificar que todos os lugares estão vazios ou preenchidos com hints
            if board[row][left] not in ["", "L"] or board[row][right] not in ["", "R"]:
                return False
            for col in cols:
                if col not in [left,right]:
                    if board[row][col] not in  ["", "M"]:
                        return False
                #verificar que cabe na contagem de cada coluna   
                if COL[col] - 1 < 0: 
                    return False

            #raio 1
            r1 = self.values(info)
            for x in r1:
                if x not in ["w", "W", "", "Non-existant"]:
                    return False

            #raio 2
            #linha de cima 
            above = self.top2(row+1,left) + self.top2(row+1,right)
            for x in above:
                if x == "T" or x == "t":
                    return False   
            #linha do lado direito 
            sider = self.right2(row,right+1)
            for x in sider:
                if x == "R" or x == "r":
                    return False    
            #linha de baixo 
            below = self.bottom2(row-1,left) + self.bottom2(row-1,right)
            for x in below:
                if x == "B" or x == "b":
                    return False  
            #linha do lado esquerdo
            sidel = self.left2(row, left-1)
            for x in sidel:
                if x == "L" or x == "l":
                    return False
                    

        if item == "cboat":
            rows = coord[0]
            col = coord[1]
            boatdim=len(rows)
            top = rows[0]
            bottom = rows[-1]
            #verifica se cabe na contagem da coluna e se as posições são válidas e se ainda pode pôr esse tamanho de barco
            if bottom >= dim or top < 0 or COL[col] - boatdim < 0 or  boats[str(boatdim)] == 0:
                return False
            
            #verificar que todos os lugares estão vazios ou preenchidos com hints
            if board[top][col] not in ["", "T"] or board[bottom][col] not in ["", "B"]:
                return False
            for row in rows:
                if row not in [top,bottom]:
                    if board[row][col] not in ["","M"]:
                        return False
                #verificar que cabe na contagem de cada linha
                if ROW[row] - 1 < 0:
                    return False
                
            #raio 1
            r1 = self.values(info)
            for x in r1:
                if x not in ["w", "W", "", "Non-existant"]:
                    return False

            #raio 2
            # linha de cima  
            above = self.top2(top-1,col) 
            for x in above:                    
                if x == "T" or x == "t":
                    return False   
            #linha do lado direito
            sider = self.right2(top,col+1) + self.right2(bottom,col+1) 
            for x in sider:                    
                if x == "R" or x == "r":
                    return False    
            #linha de baixo 
            below = self.bottom2(bottom+1,col)
            for x in below:
                if x == "B" or x == "b":
                    return False  
            #linha do lado esquerdo 
            sidel = self.left2(top,col-1) + self.left2(bottom,col-1) 
            for x in sidel:
                if x == "L" or x == "l":
                    return False
                    
        return True
    


    def printboard(self):
        """devolve o tabuleiro no output desejado"""
        dim = self.dim
        board = self.mboard
        final = ""
        for i in range(dim):
            for j in range(dim):
                if board[i][j] == "w":
                    final += "."
                else:
                    final += board[i][j]
            final += "\n"
        return final[:-1]



    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        i=0
        h=[]
        for line in sys.stdin:
            line = line.split()
            if i==0:
                dim = len(line) -1
                row = [int(x) for x in line[1:]] #criar contagem das linhas
            elif i==1:
                col = [int(x) for x in line[1:]] #criar contagem das colunas
            elif i>2:
                h = h + [[int(line[1])] + [int(line[2])] + [line[-1]]] #criar lista das hints
            i+=1

        #criar matriz que representa o tabuleiro e preenchê-la com hints
        mboard = [["" for j in range(dim)] for i in range(dim)] 
        for hint in h:
            posi = hint[0]
            posj = hint[1]
            mboard[posi][posj] = hint[2]
   
        #criar dicionário com barcos a preencher
        boats = {"1" : 4, "2" : 3, "3" : 2, "4" : 1} 

        B = Board(row, col, h, boats, mboard)
        return B



#---------------------------------------------------------------------------------------------------------



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)
        


    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        """actions possíveis:
        -> preencher linha/coluna com agua - rwater / cwater
        -> colocar barco em linha ou coluna - rboat / cboat """

        actions = []
        board = state.board
        dim = board.dim
        row = board.row
        col = board.col
        boats = board.boats

        #enquanto a lista de hints não estiver vazia, devolver apenas ações possíveis para a última hint da lista
        if board.hints != [] and not all([h[-1] == "W" for h in board.hints]):
            hint = board.hints.pop()
            #se a hint for "W", pass e ir buscar próxima
            if hint[-1] == "W":
                while hint[-1] == "W" and board.hints != []:
                    hint = board.hints.pop()
            
            i=hint[0]
            j=hint[1]
            if hint[-1] == "C":
                actions.append(("C", [i,j]))

            elif hint[-1] == "T":
                #verificar que não preenchemos 2 vezes o mesmo barco
                for h in board.hints[:]:
                    if h[-1] == "B" and h[1] == hint[1] and h[0] in [hint[0]+1, hint[0]+2, hint[0]+3]:
                        board.hints.remove(h) 
                    if h[-1] == "M" and h[1] == hint[1] and h[0] in [hint[0]+1, hint[0]+2]:
                        board.hints.remove(h)

                if board.canput(("cboat", [[i,i+1,i+2,i+3],j])):
                    actions.append(("cboat", [[i,i+1,i+2,i+3],j]))
                if board.canput(("cboat", [[i,i+1,i+2],j])):
                    actions.append(("cboat", [[i,i+1,i+2],j]))
                if board.canput(("cboat", [[i,i+1],j])):
                    actions.append(("cboat", [[i,i+1],j]))


            elif hint[-1] == "B":
                #verificar que não preenchemos 2 vezes o mesmo barco
                for h in board.hints[:]:
                    if h[-1] == "T" and h[1] == hint[1] and h[0] in [hint[0]-1, hint[0]-2, hint[0]-3]:
                        board.hints.remove(h) 
                    if h[-1] == "M" and h[1] == hint[1] and h[0] in [hint[0]-1, hint[0]-2]:
                        board.hints.remove(h)

                if board.canput(("cboat", [[i-3,i-2,i-1,i],j])):
                    actions.append(("cboat", [[i-3,i-2,i-1,i],j]))
                if board.canput(("cboat", [[i-2,i-1,i],j])):
                    actions.append(("cboat", [[i-2,i-1,i],j]))
                if board.canput(("cboat", [[i-1,i],j])):
                    actions.append(("cboat", [[i-1,i],j]))
                
            elif hint[-1] == "L":
                #verificar que não preenchemos 2 vezes o mesmo barco
                for h in board.hints[:]:
                    if h[-1] == "R" and h[0] == hint[0] and h[1] in [hint[1]+1, hint[1]+2, hint[1]+3]:
                        board.hints.remove(h) 
                    if h[-1] == "M" and h[0] == hint[0] and h[1] in [hint[1]+1, hint[1]+2]:
                        board.hints.remove(h)

                if board.canput(("rboat", [i,[j,j+1,j+2,j+3]])):
                    actions.append(("rboat", [i,[j,j+1,j+2,j+3]]))
                if board.canput(("rboat", [i,[j,j+1,j+2]])):
                    actions.append(("rboat", [i,[j,j+1,j+2]])) 
                if board.canput(("rboat", [i,[j,j+1]])):
                    actions.append(("rboat", [i,[j,j+1]]))
                
            elif hint[-1] == "R":
                #verificar que não preenchemos 2 vezes o mesmo barco
                for h in board.hints[:]:
                    if h[-1] == "L" and h[0] == hint[0] and h[1] in [hint[1]-1, hint[1]-2, hint[1]-3]:
                        board.hints.remove(h) 
                    if h[-1] == "M" and h[0] == hint[0] and h[1] in [hint[1]-1, hint[1]-2]:
                        board.hints.remove(h)

                if board.canput(("rboat", [i,[j-3,j-2,j-1,j]])):
                    actions.append(("rboat", [i,[j-3,j-2,j-1,j]]))
                if board.canput(("rboat", [i,[j-2,j-1,j]])):
                    actions.append(("rboat", [i,[j-2,j-1,j]]))
                if board.canput(("rboat", [i,[j-1,j]])):
                    actions.append(("rboat", [i,[j-1,j]]))
                

            elif hint[-1] == "M":
                #verificar que não preenchemos 2 vezes o mesmo barco
                for h in board.hints[:]:
                    if h[-1] == "L" and h[0] == hint[0] and h[1] in [hint[1]-1, hint[1]-2]:
                        board.hints.remove(h) 
                    if h[-1] == "R" and h[0] == hint[0] and h[1] in [hint[1]+1, hint[1]+2]:
                        board.hints.remove(h) 
                    if h[-1] == "T" and h[1] == hint[1] and h[0] in [hint[0]-1, hint[0]-2]:
                        board.hints.remove(h) 
                    if h[-1] == "B" and h[1] == hint[1] and h[0] in [hint[0]+1, hint[0]+2]:
                        board.hints.remove(h) 
                    if h[-1] == "M":
                        if h[0] == hint[0] and h[1] in [hint[1]-1, hint[1]+1]:
                            board.hints.remove(h)
                        if h[1] == hint[1] and h[0] in [hint[0]+1, hint[0]-1]:
                            board.hints.remove(h) 
                        
                #verifica se pode colocar barco de 3
                if board.canput(("rboat", [i,[j-1,j,j+1]])):
                    actions.append(("rboat", [i,[j-1,j,j+1]]))
                #verifica se pode colocar barco de 4 mais à direita
                if board.canput(("rboat", [i,[j-1,j,j+1,j+2]])):
                    actions.append(("rboat", [i,[j-1,j,j+1,j+2]]))
                #verifica se pode colocar barco de 4 mais à esquerda
                if board.canput(("rboat", [i,[j-2,j-1,j,j+1]])):
                    actions.append(("rboat", [i,[j-2,j-1,j,j+1]]))
                #verifica se pode colocar barco de 3
                if board.canput(("cboat", [[i-1,i,i+1],j])):
                    actions.append(("cboat", [[i-1,i,i+1],j]))
                #verifica se pode colocar barco de 4 mais em baixo
                if board.canput(("cboat", [[i-1,i,i+1,i+2],j])): 
                    actions.append(("cboat", [[i-1,i,i+1,i+2],j]))
                #verifica se pode colocar barco de 4 mais em cima
                if board.canput(("cboat", [[i-2,i-1,i,i+1],j])):
                    actions.append(("cboat", [[i-2,i-1,i,i+1],j]))
                

        #apenas quando lista de hints estiver vazia, verifica ações correspondentes a preencher barcos, do maior para o menor   
        elif boats["4"] > 0:
            for i in range(dim):
                for j in range(dim):
                    if board.canput(("rboat", [i,[j,j+1,j+2,j+3]])):
                        actions.append(("rboat", [i,[j,j+1,j+2,j+3]]))
                    if board.canput(("cboat", [[i,i+1,i+2,i+3],j])):
                        actions.append(("cboat", [[i,i+1,i+2,i+3],j]))
            
        elif boats["3"] > 0:
            for i in range(dim):
                for j in range(dim):
                    if board.canput(("rboat", [i,[j,j+1,j+2]])):
                        actions.append(("rboat", [i,[j,j+1,j+2]]))
                    if board.canput(("cboat", [[i,i+1,i+2],j])):
                        actions.append(("cboat", [[i,i+1,i+2],j]))

        elif boats["2"] > 0:
            for i in range(dim):
                for j in range(dim):
                    if board.canput(("rboat", [i,[j,j+1]])):
                        actions.append(("rboat", [i,[j,j+1]]))
                    if board.canput(("cboat", [[i,i+1],j])):
                        actions.append(("cboat", [[i,i+1],j]))

        elif boats["1"] > 0:
            for i in range(dim):
                for j in range(dim):
                    if board.canput(("c", [i,j])):
                        actions.append(("c", [i,j]))

        #quando todos os barcos estiverem colocados, encher as restantes posições com água
        else:
            for i in range(dim):
                if row[i] == 0:
                    return [("rwater", i)] 

             
        return actions

            



    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        act =  action[0]
        coord = action[1]
        currentboard = state.board
        #cria uma cópia independente do tabuleiro
        newboard = Board(currentboard.row[:], currentboard.col[:], currentboard.hints[:], currentboard.boats.copy(), [x[:] for x in currentboard.mboard])

        if act == "rwater":
            newboard.fillwater_row(coord)
            
        elif act == "cwater":
            newboard.fillwater_col(coord)

        else:
            newboard.fill(action)

        newstate = BimaruState(newboard)
        return newstate
    




    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = state.board
        mboard = board.mboard
        dim = board.dim
        boats = board.boats
        #verifica que todos os barcos foram colocados
        if any([x != 0 for x in boats.values()]):
            return False
        #verifica que todas as posições estão preenchidas
        i=0
        while i < dim:
            j=0
            while j < dim:
                if mboard[i][j] == "":
                    return False

                j+=1
            i+=1

        return True



    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""

        pass
    



if __name__ == "__main__":
    import timeit
    start = timeit.default_timer()

    board=Board.parse_instance()
    problem1 = Bimaru(board)
    Final = depth_first_tree_search(problem1)
    print(Final.state.board.printboard())
    
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
    
##demora cerca de 3 segundos a correr:
##$ python3 bimaru.py < instance10.txt

