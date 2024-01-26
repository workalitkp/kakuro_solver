class Board:
    def __init__(self,length,height,y_index,x_index) -> None:
        self.length = length
        self.height = height
        self.x_index = x_index
        self.y_index = y_index
        self.board = []
        if(len(y_index) != self.length or len(x_index) != self.height):
            return "Error: Index does not match board size"
        # self.board.append(x_index)
        for i in range(height):
            self.board.append([0]*length)

    def __str__(self) -> str:
        return str(self.board)


class Solver:
    def __init__(self,board,values,target) -> None:
        self.board = board
        self.values = values
        self.res = []
        self.grid = [[0,0,0],[0,0,0],[0,0,0]]
        
        self.eval_board(self.board)
        # self.backtrack([],0,target)
        # do self.clean_up() until lists cant be more optimized
        while True:
            x_index_copy = self.board.x_index.copy()
            y_index_copy = self.board.y_index.copy()
            self.clean_up()
            if x_index_copy == self.board.x_index and y_index_copy == self.board.y_index:
                break
        self.solve()
    def eval_board(self,board):
        for i in range(len(board.y_index)):
            self.res = []
            y_res = self.backtrack([],0,board.y_index[i])
            board.y_index[i] = [board.y_index[i],len(y_res),y_res]

        for j in range(len(board.x_index)):
            self.res = []
            x_res = self.backtrack([],0,board.x_index[j])
            board.x_index[j] = [board.x_index[j],len(x_res),x_res]
        return board

    def backtrack(self,cur,pos,target):
        if target == 0 and len(cur)==3:
            self.res.append(cur.copy())
            # return
        if target <= 0:
            return
        prev = -1
        for i in range(pos,len(self.values)):
            if (values[i] == prev):
                continue
            cur.append(self.values[i])
            self.backtrack(cur,i+1,target-self.values[i])
            cur.pop()
            prev = self.values[i]
        return self.res
        # min_node = min(self.board.y_index+self.board.x_index,key=lambda x: x[1])
    def uniqe_values(self,combinations):
        lll = []
        for i in combinations:
            lll += i
        uniqe = set(lll)
        return uniqe

    def clean_up(self):
        min_node = min(self.board.y_index+self.board.x_index,key=lambda x: x[1])
        uniqe_min = self.uniqe_values(min_node[2])
        if min_node in self.board.y_index:
            for cnt in range(len(self.board.x_index)):
                trash = []
                for i in self.board.x_index[cnt][2]:
                    f = False
                    for j in uniqe_min:
                        if (j in i):
                            f = True
                    if(f==False):
                        trash.append(i)
                for t in trash:
                    self.board.x_index[cnt][2].remove(t)
                    self.board.x_index[cnt][1] -= 1

            
        else:
            for cnt in range(len(self.board.y_index)):
                trash = []
                for i in self.board.y_index[cnt][2]:
                    f = False
                    for j in uniqe_min:
                        if (j in i):
                            f = True
                            break
                    if(f==False):
                        trash.append(i)
                for t in trash:
                    self.board.y_index[cnt][2].remove(t)
                    self.board.y_index[cnt][1] -= 1
    def duplicate(self,com1,com2):
        for i in com1:
            if i in com2:
                return i
        for i in com2:
            if i in com1:
                return i
        return False
    def solve(self):
        for i in range(len(self.board.y_index)):
            for j in range(len(self.board.x_index)):
                if self.board.y_index[i][1] == 1 and self.board.x_index[j][1] == 1:
                    if(self.grid[i][j] != 0):
                        continue
                    dup = self.duplicate(self.board.y_index[i][2][0],self.board.x_index[j][2][0])
                    if dup:
                        self.grid[i][j] = dup
                        self.board.y_index[i][2][0].remove(dup)
                        self.board.x_index[j][2][0].remove(dup)
                        for i in range(3):
                            print(self.grid[i])
                        print("------")

        # Check if the board is solved  
            # if not self.is_solved():
                # self.solve()

    def is_solved(self):
        for i in range(len(self.board.y_index)):
            for j in range(len(self.board.x_index)):
                if self.board.y_index[i][1] != 0 or self.board.x_index[j][1] != 0:
                    return False
        return True
    def __str__(self) -> str:
        return str(self.board.x_index) + '\n' + str(self.board.y_index)


board = Board(3,3,y_index=[20,18,9],x_index=[23,17,7])
values = [1,2,3,4,5,6,7,8,9]

solver = Solver(board,values,23)
print(solver)