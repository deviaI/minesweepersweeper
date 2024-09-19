import random as rng
import time

rows = 8
cols = 10
num_bmbs = 10


def generate_random_board(show=True):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    pos = []
    while len(pos) < num_bmbs:
        x = rng.randint(0, 79)
        while x in pos:
            x = rng.randint(0, 79)
        pos.append(x)
    for index in pos:
        i = index // cols
        j = index % cols
        board[i][j] = "x"
    for i in range(0, rows):
        for j in range(0, cols):
            if board[i][j] != "x":
                bc = 0
                for n in range(-1, 2):
                    for m in range(-1, 2):
                        try:
                            if board[i + n][j + m] == "x" and i + n >= 0 and j + m >= 0:
                                bc += 1
                        except IndexError:
                            pass
                board[i][j] = bc
    if show:
        print_board(board)
    return board


def print_board(board):
    print("######################")
    board_str = [[str(item) for item in row] for row in board]
    col_widths = [max(len(item) for item in col) for col in zip(*board_str)]
    for row in board_str:
        print("  ".join(item.ljust(width) for item, width in zip(row, col_widths)))
    print("######################")


def find_first_empty(board):
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 0:
                return i, j


def find_connected_empties(i, j, board):
    if board[i][j] != 0:
        return board
    board[i][j] = "E"
    for n in range(-1, 2):
        for m in range(-1, 2):
            if rows > i + n >= 0 and cols > j + m >= 0:
                board = find_connected_empties(i + n, j + m, board)
    return board


def final_check(board):
    for i in range(rows):
        for j in range(cols):
            if not isinstance(board[i][j], str):
                if not check_adj(board, i, j):
                    return False, i, j
    return True, -1, -1


def check_adj(board, i, j):
    for n in range(-1, 2):
        for m in range(-1, 2):
            if rows > i + n >= 0 and cols > j + m >= 0:
                if board[i + n][j + m] == "E":
                    return True
    return False


def random_trial(N, show_all=False, show_ocs=False, verif=[False, 0, 0]):
    verif_1 = 0
    verif_2 = 0
    rng.seed(int(time.time() * 1000))
    ctr = 0
    l_n_E = []
    for l in range(1, N + 1):
        ocs_1 = True
        rand_board = generate_random_board(show_all)
        i, j = find_first_empty(rand_board)
        checked_board = find_connected_empties(i, j, rand_board)
        if show_all:
            print_board(checked_board)
        k = 0
        for row in checked_board:
            if 0 in row:
                ocs_1 = False
                if verif[0] and verif_1 < verif[1]:
                    verif_1 += 1
                    print("Board below failed condition 1 at row " + str(k+1))
                    print_board(checked_board)
                break
            k += 1
        if ocs_1:
            fc, i_f, j_f = final_check(checked_board)
            if fc:
                if show_ocs:
                    print("Board below successfully checked")
                    print_board(checked_board)
                ctr += 1
                n_E = 0
                for row in checked_board:
                    n_E += row.count("E")
                l_n_E.append(n_E)
            else:
                if verif[0] and verif_2 < verif[2]:
                    verif_2 += 1
                    print("Board below failed condition 2 at " + str(i_f) + ", " + str(j_f))
                    print_board(checked_board)
    if ctr == 0:
        print("Checked " + str(l) + " random boards")
        print("Found " + str(ctr) + " boards with possible one click solves")
        print("Odds of getting a one click solvable board: <" + str(1 / l))

    else:
        avg_E = sum(l_n_E) / len(l_n_E)
        print("Checked " + str(l) + " random boards")
        print("Found " + str(ctr) + " boards with possible one click solves")
        print("Odds of getting a one click solvable board: " + str(ctr / l))
        print("Average number of empty tiles in a one-click-solvable board: " + str(avg_E))
        print("Odds of successful one-click-solve of a ocs board: " + str(avg_E / (rows * cols)))
        print("Overall odds of getting a one-click-solvable board AND winning it in one click: " + str(
            (ctr / l) * (avg_E / (rows * cols))))


random_trial(100000, show_all=False, show_ocs=False, verif=[True, 10, 10])
