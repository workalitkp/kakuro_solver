class Config:
    EMPTY = "#"
    UNKNOWN = "?"
    SEP = "\\"


class Node:
    def __init__(
        self,
        x: int,
        y: int,
        right: int | str,
        space_right: int,
        down: int | str,
        space_down: int,
    ) -> None:
        self.x = x
        self.y = y
        self.right = right
        self.down = down
        self.space_right = space_right if isinstance(self.right, int) else 0
        self.space_down = space_down
        self.combinations_right = (
            self.find(self.right, self.space_right)
            if isinstance(self.right, int)
            else []
        )
        self.combinations_down = (
            self.find(self.down, self.space_down) if isinstance(self.down, int) else []
        )
        self.value_right = (
            [0 for i in range(self.space_right)] if isinstance(self.right, int) else []
        )
        self.value_down = (
            [0 for i in range(self.space_down)] if isinstance(self.down, int) else []
        )

    @property
    def space_down(self):
        return self._space_down

    @space_down.setter
    def space_down(self, value):
        if isinstance(self.down, str):
            self._space_down = 0
            return
        self._space_down = value
        self.value_down = (
            [0 for i in range(self.space_down)] if isinstance(self.down, int) else []
        )
        self.combinations_down = (
            self.find(self.down, self.space_down) if isinstance(self.down, int) else []
        )
        self.check_value("down")

    @property
    def space_right(self):
        return self._space_right

    @space_right.setter
    def space_right(self, value):
        if isinstance(self.right, str):
            self._space_right = 0
            return
        self._space_right = value
        self.value_right = (
            [0 for i in range(self.space_right)] if isinstance(self.right, int) else []
        )
        self.combinations_right = (
            self.find(self.right, self.space_right)
            if isinstance(self.right, int)
            else []
        )

    @property
    def combinations_right(self):
        return self._combinations_right

    @combinations_right.setter
    def combinations_right(self, value):
        self._combinations_right = value
        self.check_value("right")

    @property
    def combinations_down(self):
        return self._combinations_down

    @combinations_down.setter
    def combinations_down(self, value):
        self._combinations_down = value
        self.check_value("down")

    def check_value(self, direction: str = "right"):
        # if there is same value for all combinations in direction in specific index
        # replace it with self.value[index]
        if direction == "right":
            for i in range(len(self.combinations_right)):
                for j in range(len(self.combinations_right[i])):
                    flag = True
                    for k in range(len(self.combinations_right)):
                        if (
                            self.combinations_right[i][j]
                            != self.combinations_right[k][j]
                        ):
                            flag = False
                            break
                    if flag:
                        # print(self, self.combinations_right[i][j], self.combinations_right[k][j])
                        self.value_right[j] = self.combinations_right[i][j]
        elif direction == "down":
            for i in range(len(self.combinations_down)):
                for j in range(len(self.combinations_down[i])):
                    flag = True
                    for k in range(len(self.combinations_down)):
                        if self.combinations_down[i][j] != self.combinations_down[k][j]:
                            flag = False
                            break
                    if flag:
                        self.value_down[j] = self.combinations_down[i][j]

    def __repr__(self):
        return f"({self.down}\{self.right})"


    def __str__(self) -> str:
        return self.__repr__()

    def find_combinations(self, value: int, space: int, combination: list):
        if space == 0 and value == 0:
            self._combinations.append(combination)
            return
        if 0 == space or value < 0:
            return
        for i in range(1, 10):
            if i not in combination:
                self.find_combinations(value - i, space - 1, combination + [i])

    def find(self, value, space):
        self._combinations = []
        self.find_combinations(value, space, [])
        return self._combinations.copy()


class Board:
    def __init__(self, board) -> None:
        self.board = board

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        if isinstance(value, Board):
            self.board = value.board
        self._board = value
        self._board = self.create_board(self._board)

    def create_board(self, text: str):
        board = []
        for i in text.strip().split("\n"):
            board2 = []
            count = 0
            for j in i.strip().split():
                count += 1
                if j.strip() == Config.EMPTY:
                    node = Node(len(board), count, Config.EMPTY, 0, Config.EMPTY, 0)
                elif "\\" in j:
                    j1 = j.split(Config.SEP)[0]
                    j2 = j.split(Config.SEP)[1]
                    if j1 != Config.EMPTY:
                        j1 = int(j1)
                    if j2 != Config.EMPTY:
                        j2 = int(j2)
                    node = Node(len(board), count, j2, 0, j1, 0)
                elif j.strip() == Config.UNKNOWN:
                    node = Node(len(board), count, Config.UNKNOWN, 0, Config.UNKNOWN, 0)
                board2.append(node)
            board.append(board2)
        return board

    def __str__(self) -> str:
        text = ""
        for i in self.board:
            for j in i:
                text += str(j) + "\t"
            text += "\n"
        return text

    def remove_non_intersection(
        self, x: int, y: int, node1: Node, node2: Node
    ) -> (Node, Node):
        uniqe = []
        uniqe2 = []

        for i in node1.combinations_right:
            for j in i:
                if j not in uniqe:
                    uniqe.append(j)
        for i in node2.combinations_down:
            for j in i:
                if j not in uniqe2:
                    uniqe2.append(j)

        intersection = []
        for i in uniqe:
            if i in uniqe2 and i:
                intersection.append(i)
        # print(intersection)
        resy1 = []
        for i in intersection:
            for j in node1.combinations_right:
                if i in j and j.index(i) == x:
                    resy1.append(j)
        resy2 = []
        for i in intersection:
            for j in node2.combinations_down:
                if i in j and j.index(i) == y:
                    resy2.append(j)
        # print(node1.combinations_right)
        node1.combinations_right = resy1
        node2.combinations_down = resy2
        return node1, node2


# x1, x2 = remove_non_intersection(1, find(2, 14), 0, find(2, 6), [0, 0], [0, 0])
# print(x1)
# print("***************")
# print(x2)

text = """
# # # 24\\# 16\\#
# # 6\\17 ? ?
# 17\\18 ? ? ?
#\\17 ? ? ? #
#\\11 ? ? # #
"""
board = Board(text)
n1 = Node(0, 0, "#", 0, 16, 2)
n2 = Node(1, 0, 17, 2, "#", 0)
n3 = Node(0, 1, "#", 0, 10, 2)
n4 = Node(1, 1, 9, 2, "#", 0)
# n5 = Node(0,1,'#',0,15,3)
# n6 = Node(0,0,'#',0,23,3)
print("-----------------------------------")
for i in [n1, n3]:
    print("down", i, i.combinations_down)
    print("value_down", i, i.value_down)
for i in [n2, n4]:
    print("right", i, i.combinations_right)
    print("value_right", i, i.value_right)

for i in range(0, 5):
    n1, n2 = board.remove_non_intersection(0, 0, n1, n2)
    n1, n4 = board.remove_non_intersection(0, 1, n1, n4)
    n3, n2 = board.remove_non_intersection(1, 0, n3, n2)
    n3, n4 = board.remove_non_intersection(1, 1, n3, n4)
