text = """
# # # 24\\# 16\\#
# # 6\\17 ? ?
# 17\\18 ? ? ?
#\\17 ? ? ? #
#\\11 ? ? # #
"""

board = []
for i in text.strip().split('\n'):
    for j in i.strip().split():
        if j.strip() == '#':
            board.append(['#','#'])
        elif '\\' in j:
            j1 = j.split('\\')[0]
            j2 = j.split('\\')[1]
            if j1 != '#':
                j1 = int(j1)
            if j2 != '#':
                j2 = int(j2)
            board.append([j1,j2])
        elif j.strip() == '?':
            board.append(['?','?'])
for i in range(len(board)):
    print(board[i])