"""
Starter Code for Assignment 1 - COMP 8085
Please do not redistribute this code our your solutions
The game engine to keep track of the game and provider of a generic AI implementation
 You need to extend the GenericAI class to perform a better job in searching for the next move!
"""
# pip install Chessnut

from Chessnut import Game
import random
import time
import math
import re
import json
import sys

sys.setrecursionlimit(2147483647)

def create_generator(g_list):
    for num in g_list:
        yield num
    yield "done"

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

class AIEngine:
    def __init__(self, board_state, reasoning_depth=3):
        self.game = Game(board_state)
        # TODO call the proper implementation of AI (e.g. MinimaxAI) instead of GenericAI
        self.computer = GenericAI(self.game, reasoning_depth)
        #self.computer = MinimaxAI(self.game, reasoning_depth)
        #self.computer = IterativeDeepeningAI(self.game, reasoning_depth)
        #self.computer = MCTSAI(self.game, reasoning_depth)

    def prompt_user(self):
        self.computer.print_board(str(self.game))
        parent = str(self.game).split()[0] +" "+ str(self.game).split()[1]
        dataDict = {}
        if str(type(self.computer).__name__) == "MCTSAI":
            try:
                dataDict = json.load(open("database.txt"))
            except:
                dataDict.update({parent: []})
            if not dataDict:
                dataDict.update({parent: []})
        try:
            while self.game.status < 2:
                stateArr = str(self.game).split()

                if not re.search("[a-jl-zA-JL-Z]",stateArr[0]):
                    break

                user_move = input("\nMake a move: \033[95m")
                print("\033[0m")
                while user_move not in self.game.get_moves() and user_move != "ff":
                    user_move = input("Please enter a valid move: ")
                if user_move == "ff":
                    print("Execution Stopped!")
                    break
                self.game.apply_move(user_move)
                stateArr = str(self.game).split()

                if not re.search("[a-jl-zA-JL-Z]",stateArr[0]):
                    break
                captured = self.captured_pieces(str(self.game))
                start_time = time.time()
                self.computer.print_board(str(self.game), captured)
                print("\nComputer Playing...\n")
                if self.game.status < 2:
                    current_state = str(self.game)
                    if str(type(self.computer).__name__) == "MCTSAI":
                        computer_move, dataDict = self.computer.make_move(current_state, dataDict, "Player")
                    else:
                        computer_move = self.computer.make_move(current_state)
                    piece_name = {'p': 'pawn', 'b': 'bishop', 'n': 'knight', 'r': 'rook', 'q': 'queen', 'k': 'king'}
                    start = computer_move[:2]
                    end = computer_move[2:4]
                    piece = piece_name[self.game.board.get_piece(self.game.xy2i(computer_move[:2]))]
                    captured_piece = self.game.board.get_piece(self.game.xy2i(computer_move[2:4]))
                    if captured_piece != " ":
                        captured_piece = piece_name[captured_piece.lower()]
                        print("---------------------------------")
                        print("Computer's \033[92m{piece}\033[0m at \033[92m{start}\033[0m captured \033[91m{captured_piece}\033[0m "
                              "at \033[91m{end}\033[0m.".format(piece=piece, start=start, captured_piece=captured_piece, end=end))
                        print("---------------------------------")
                    else:
                        print("---------------------------------")
                        print("Computer moved \033[92m{piece}\033[0m at \033[92m{start}\033[0m to \033[92m{end}\033[0m.".format(
                            piece=piece, start=start, end=end))
                        print("---------------------------------")
                    print("\033[1mNodes visited:\033[0m        \033[93m{}\033[0m".format(self.computer.node_count))
                    print("\033[1mElapsed time in sec:\033[0m  \033[93m{time}\033[0m".format(time=time.time() - start_time))
                    self.game.apply_move(computer_move)
                captured = self.captured_pieces(str(self.game))
                self.computer.print_board(str(self.game), captured)
            print("Game Ended!")
        except KeyboardInterrupt:
            print("Execution Stopped!")

    def prompt_ai(self):
            self.computer.print_board(str(self.game))
            parent = str(self.game).split()[0] +" "+ str(self.game).split()[1]
            status = 0
            dataDict = {}
            listOfAllMoves = []
            try:
                dataDict = json.load(open("database.txt"))
            except:
                dataDict.update({parent: []})
            if not dataDict:
                dataDict.update({parent: []})
            try:
                while self.game.status < 2:
                    status = self.game.status

                    stateArr = str(self.game).split()

                    if not re.search("[a-jl-zA-JL-Z]",stateArr[0]):
                        status = 3
                        break
                    user_move = MCTSAI(self.game, 3)
                    if str(type(self.computer).__name__) == "MCTSAI":
                        user_move, dataDict = user_move.make_move(str(self.game), dataDict, "MCTSAI")
                    else:
                        user_move, dataDict = user_move.make_move(str(self.game), dataDict, "Player")

                    print("\033[0m")
                    while user_move not in self.game.get_moves() and user_move != "ff":
                        user_move = MCTSAI(self.game, 3)
                    if user_move == "ff":
                        print("Execution Stopped!")
                        break
                    self.game.apply_move(user_move)
                    listOfAllMoves.append(str(self.game).split()[0] +" "+ str(self.game).split()[1])

                    stateArr = str(self.game).split()
                    if not re.search("[a-jl-zA-JL-Z]",stateArr[0]):
                        status = 3
                        break
                    # child = str(self.game)
                    # if child not in dataDict[parent]:
                    #     dataDict[parent].append(child)
                    #     dataDict.update({child: []})
                    # parent = child

                    captured = self.captured_pieces(str(self.game))
                    start_time = time.time()
                    self.computer.print_board(str(self.game), captured)
                    print("\nComputer Playing...\n")
                    if self.game.status < 2:
                        current_state = str(self.game)
                        if str(type(self.computer).__name__) == "MCTSAI":
                            computer_move, dataDict = self.computer.make_move(current_state, dataDict, "MCTSAI")
                        else:
                            computer_move = self.computer.make_move(current_state)
                        piece_name = {'p': 'pawn', 'b': 'bishop', 'n': 'knight', 'r': 'rook', 'q': 'queen', 'k': 'king'}
                        start = computer_move[:2]
                        end = computer_move[2:4]
                        piece = piece_name[self.game.board.get_piece(self.game.xy2i(computer_move[:2]))]
                        captured_piece = self.game.board.get_piece(self.game.xy2i(computer_move[2:4]))
                        if captured_piece != " ":
                            captured_piece = piece_name[captured_piece.lower()]
                            print("---------------------------------")
                            print("Computer's \033[92m{piece}\033[0m at \033[92m{start}\033[0m captured \033[91m{captured_piece}\033[0m "
                                "at \033[91m{end}\033[0m.".format(piece=piece, start=start, captured_piece=captured_piece, end=end))
                            print("---------------------------------")
                        else:
                            print("---------------------------------")
                            print("Computer moved \033[92m{piece}\033[0m at \033[92m{start}\033[0m to \033[92m{end}\033[0m.".format(
                                piece=piece, start=start, end=end))
                            print("---------------------------------")
                        print("\033[1mNodes visited:\033[0m        \033[93m{}\033[0m".format(self.computer.node_count))
                        print("\033[1mElapsed time in sec:\033[0m  \033[93m{time}\033[0m".format(time=time.time() - start_time))
                        self.game.apply_move(computer_move)
                        listOfAllMoves.append(str(self.game).split()[0] +" "+ str(self.game).split()[1])
                    captured = self.captured_pieces(str(self.game))
                    self.computer.print_board(str(self.game), captured)
                    status = self.game.status

                self.computer.print_board(str(self.game), captured)
                print(self.game)
                if str(type(self.computer).__name__) == "MCTSAI":
                    status = self.game.status
                    if not self.game.get_moves():
                        status = 2
                    print("Game Ended!")
                    stateArr = str(self.game).split()
                    if stateArr[1] == "b" and status == 2:
                        print("Winner is White!")
                        status = -1
                        for move in listOfAllMoves:
                            dataDict[move][0] += status
                    elif(status == 2):
                        print("Winner is Black!")
                        status = 1
                        for move in listOfAllMoves:
                            dataDict[move][1] += status
                    else:
                        status = 0.001
                        for move in listOfAllMoves:
                            dataDict[move][2] += status
                    # parent = str(self.game).split()[0] +" "+ str(self.game).split()[1]
                    # child = status
                    # if child not in dataDict[parent]:
                    #     dataDict[parent].append(child)
                    #     dataDict.update({child: []})
                    print(status)
                    print(self.game.status)
                    print(self.game.state)
                    print(self.game)
                    # parent = parent.children[-1]
                    # child = Node(status)
                    
                    f = open("database.txt", "w+")
                    f.write(json.dumps(dataDict))
                    f.close()
            except KeyboardInterrupt:
                print("Execution Stopped!")
                # self.inorderTraversal(firstparent, -1, "")

    def inorderTraversal(self, root, aDict):
        # print(root.data)
        # print(root.children)
        #print("Called")
        # arr2 = []
        #arr.insert(depth,[])
        #print("Called")
        #index = int(root.data.split()[-1])-1

        # try:
        #     if arr[index]:
        #         f = ""
        # except IndexError:
        #     arr.insert(index,[])
        # arr[index].append(root.data)
        aDict.update({root.data: []})
        for child in root.children:
            #text = self.inorderTraversal(child, depth, text)
            # arr2.append(child.data)
            #arr[depth].append(child.data)
            aDict = self.inorderTraversal(child, aDict)
            aDict[root.data].append(child.data)
        # for i in range(depth):
        #     text += "\t"
        # text += root.data
        # text += "\n"
        # print(root.data)
        #arr.append(root.data)
        return aDict
            

    @staticmethod
    def captured_pieces(board_state):
        piece_tracker = {'P': 8, 'B': 2, 'N': 2, 'R': 2, 'Q': 1, 'K': 1, 'p': 8, 'b': 2, 'n': 2, 'r': 2, 'q': 1, 'k': 1}
        captured = {"w": [], "b": []}
        for char in board_state.split()[0]:
            if char in piece_tracker:
                piece_tracker[char] -= 1
        for piece in piece_tracker:
            if piece_tracker[piece] > 0:
                if piece.isupper():
                    captured['w'] += piece_tracker[piece] * piece
                else:
                    captured['b'] += piece_tracker[piece] * piece
            piece_tracker[piece] = 0
        return captured


class BoardNode:
    def __init__(self, board_state=None, algebraic_move=None, value=None):
        self.board_state = board_state
        self.algebraic_move = algebraic_move
        self.value = value


class GenericAI:
    def __init__(self, game, max_depth=4, leaf_nodes=None, node_count=0):
        if leaf_nodes is None:
            leaf_nodes = []
        self.max_depth = max_depth
        self.leaf_nodes = create_generator(leaf_nodes)
        self.game = game
        self.node_count = node_count

    @property
    def name(self):
        return "Dumb AI"

    def get_moves(self, board_state=None):
        if board_state is None:
            board_state = str(self.game)
        possible_moves = []
        for move in Game(board_state).get_moves():
            if len(move) < 5 or move[4] == "q":
                clone = Game(board_state)
                clone.apply_move(move)
                node = BoardNode(str(clone))
                node.algebraic_move = move
                possible_moves.append(node)
        return possible_moves

    def make_move(self, board_state):
        possible_moves = self.get_moves(board_state)
        # TODO use search algorithms to find the best move in here
        best_move = random.choice(possible_moves)
        return best_move.algebraic_move

    def print_board(self, board_state, captured=None):
        if captured is None:
            captured = {"w": [], "b": []}
        piece_symbols = {'P': '♟', 'B': '♝', 'N': '♞', 'R': '♜', 'Q': '♛', 'K': '♚', 'p': '\033[36m\033[1m♙\033[0m',
                         'b': '\033[36m\033[1m♗\033[0m', 'n': '\033[36m\033[1m♘\033[0m', 'r': '\033[36m\033[1m♖\033[0m',
                         'q': '\033[36m\033[1m♕\033[0m', 'k': '\033[36m\033[1m♔\033[0m'}
        board_state = board_state.split()[0].split("/")
        board_state_str = "\n"
        white_captured = " ".join(piece_symbols[piece] for piece in captured['w'])
        black_captured = " ".join(piece_symbols[piece] for piece in captured['b'])
        for i, row in enumerate(board_state):
            board_state_str += str(8 - i)
            for char in row:
                if char.isdigit():
                    board_state_str += " ♢" * int(char)
                else:
                    board_state_str += " " + piece_symbols[char]
            if i == 0:
                board_state_str += "   Captured:" if len(white_captured) > 0 else ""
            if i == 1:
                board_state_str += "   " + white_captured
            if i == 6:
                board_state_str += "   Captured:" if len(black_captured) > 0 else ""
            if i == 7:
                board_state_str += "   " + black_captured
            board_state_str += "\n"
        board_state_str += "  A B C D E F G H"
        self.node_count = 0
        print(board_state_str)


class MinimaxAI(GenericAI):
    def __init__(self, game, max_depth=4, leaf_nodes=None, node_count=0):
        super(MinimaxAI, self).__init__(game, max_depth, leaf_nodes, node_count)
        self.cache = {}
        self.found_in_cache = 0

    @property
    def name(self):
        return "Minimax AI"

    def make_move(self, board_state):
        # TODO re-write this code to use minimax function to pick the best move
        stateArr = board_state.split()
        if(stateArr[-1] == "1"):
            return "d7d5"
        possible_moves = self.get_moves(board_state)
        # for moves in possible_moves:
        #     print(moves.board_state)

        v, best_move = self.max_value(board_state, -math.inf, math.inf, 0)
        
        if(best_move == None):
            best_move = random.choice(possible_moves)
        # print("=====Selected=====")
        # print(best_move.board_state)
        # print(v)
        return best_move.algebraic_move
        #return super(MinimaxAI, self).make_move(board_state)

#     def minimax(self, node, alpha, beta, current_depth=0):
#         # TODO implement this function
#         pass
    def max_value(self, state, alpha, beta, current_depth=0):
        # print("In Max")
        #if(self.game.status >= 2 or current_depth >= self.max_depth):
        if(current_depth >= self.max_depth):
            return self.utility(state), None
        current_depth +=1
        #print(self.utility(state))
        v = -math.inf
        finalMove = None
        possible_moves = self.get_moves(state)
        for move in possible_moves:
            v2, move2 = self.min_value(move.board_state, alpha, beta, current_depth)
            if(v2 > v):
                v = v2
                finalMove = move
                alpha = max(alpha, v)
#             elif(v2 == v):
#                 finalMove = random.choice([finalMove, move])
#                 alpha = max(alpha, v)
            if(v >= beta):
                return v, finalMove
        return v, finalMove
    
    def min_value(self, state, alpha, beta, current_depth=0):
        # print("In Min")
        #if(self.game.status >= 2 or current_depth > self.max_depth):
        if(current_depth >= self.max_depth):
            return self.utility(state), None
        current_depth +=1
        v = math.inf
        finalMove = None
        possible_moves = self.get_moves(state)
        for move in possible_moves:
            v2, move2 = self.max_value(move.board_state, alpha, beta, current_depth)
            if(v2 < v):
                v = v2
                finalMove =  move
                beta = min(beta, v)
#             elif(v2 == v):
#                 finalMove = random.choice([finalMove, move])
#                 beta = min(beta, v)
            if(v <= alpha):
                return v, finalMove
        return v, finalMove
    
    def utility(self, state):
        stateArr = state.split()
#         print(stateArr)
        utilityValueB = (stateArr[0].count("r") * 5) + (stateArr[0].count("n") * 3) + (stateArr[0].count("b") * 3) + (stateArr[0].count("q") * 9) + (stateArr[0].count("p")) + (stateArr[0].count("k") * 40)
            
        utilityValueW = ((stateArr[0].count("R") * 5) + (stateArr[0].count("N") * 3) + (stateArr[0].count("B") * 3) + (stateArr[0].count("Q") * 9) + (stateArr[0].count("P"))) + (stateArr[0].count("K") * 40)
        # print("B " + str(utilityValueB))
        # print("W " + str(utilityValueW))
        # print("=====")
        utilityValue = utilityValueB - utilityValueW
        # print(utilityValue)
        return utilityValue
#         if(stateArr[1] == "w"):
#             #print(utilityValue)
#             utilityValue = utilityValueB - utilityValueW
# #             print("B->" + str(utilityValue))
# #             print("=====")
#             return utilityValue
        
#         elif(stateArr[1] == "b"):
#             #print(-utilityValue)
#             utilityValue = utilityValueB - utilityValueW
# #             print("W " + str(utilityValue))
# #             print("=====")
#             return utilityValue
#         return 0

# TODO use the example of MinimaxAI class definition to prepare other AI bot search algorithms

class IterativeDeepeningAI(GenericAI):
    def __init__(self, game, max_depth=4, leaf_nodes=None, node_count=0):
        super(IterativeDeepeningAI, self).__init__(game, max_depth, leaf_nodes, node_count)
        self.cache = {}
        self.found_in_cache = 0
        self.start = 0

    @property
    def name(self):
        return "Iterative Deepening AI"

    def make_move(self, board_state):
        stateArr = board_state.split()
        if(stateArr[-1] == "1"):
            return "d7d5"

        possible_moves = self.get_moves(board_state)
        self.start = time.time()
        v = -math.inf if stateArr[1] == "b" else math.inf
        best_move = None
        self.max_depth = 1
        
        # for moves in possible_moves:
        #     print(moves.board_state)
            
        while time.time() - self.start <= 15:
            temp_v, temp_best_move = self.max_value(board_state, -math.inf, math.inf, 0)
            # print("Depth: " + str(self.max_depth))
            # print(str(v) + " vs " + str(temp_v))
            # if(temp_best_move):
                # print(temp_best_move.algebraic_move)
            if time.time() - self.start >=15:
                break
            # print("=================")
            if(temp_v >= v):
                v = temp_v
                best_move = temp_best_move
            self.max_depth += 1
        
        # print("Time taken: " + str(time.time() - self.start))
        # print("Depth: " + str(self.max_depth))
        if(best_move == None):
            best_move = random.choice(possible_moves)
        # print("=====Selected=====")
        # print(best_move.board_state)
        # print(v)
        # print(best_move.algebraic_move)
        # print(best_move.value)
        return best_move.algebraic_move

    def max_value(self, state, alpha, beta, current_depth=0):
        #print("In Max")
        if(current_depth >= self.max_depth or time.time() - self.start >= 15):
            # print("Max depth: " + str(self.max_depth))
            return self.utility(state), None
        current_depth +=1
        v = -math.inf
        finalMove = None
        possible_moves = self.get_moves(state)
        for move in possible_moves:
            v2, move2 = self.min_value(move.board_state, alpha, beta, current_depth)
            if(v2 > v):
                v = v2
                finalMove = move
                alpha = max(alpha, v)
            if(v >= beta):
                return v, finalMove
        return v, finalMove
    
    def min_value(self, state, alpha, beta, current_depth=0):
        #print("In Min")
        if(current_depth >= self.max_depth or time.time() - self.start >= 15):
            return self.utility(state), None
        current_depth +=1
        v = math.inf
        finalMove = None
        possible_moves = self.get_moves(state)
        for move in possible_moves:
            v2, move2 = self.max_value(move.board_state, alpha, beta, current_depth)
            if(v2 <= v):
                v = v2
                finalMove =  move
                beta = min(beta, v)
            if(v <= alpha):
                return v, finalMove
        return v, finalMove
    
    def utility(self, state):
        stateArr = state.split()
        utilityValueB = (stateArr[0].count("r") * 5) + (stateArr[0].count("n") * 3) + (stateArr[0].count("b") * 3) + (stateArr[0].count("q") * 9) + (stateArr[0].count("p")) + (stateArr[0].count("k") * 40)
            
        utilityValueW = ((stateArr[0].count("R") * 5) + (stateArr[0].count("N") * 3) + (stateArr[0].count("B") * 3) + (stateArr[0].count("Q") * 9) + (stateArr[0].count("P"))) + (stateArr[0].count("K") * 40)
        utilityValue = utilityValueB - utilityValueW
        # print("B " + str(utilityValueB))
        # print("W " + str(utilityValueW))
        # print("=====")
        # print(utilityValue)
        return utilityValue

class MCTSAI(GenericAI):
    def __init__(self, game, max_depth=4, leaf_nodes=None, node_count=0):
        super(MCTSAI, self).__init__(game, max_depth, leaf_nodes, node_count)
        self.cache = {}
        self.found_in_cache = 0
        self.start = 0

    @property
    def name(self):
        return "Iterative Deepening AI"

    # def getValueOfMove(self, move, value, dataDict):
    #     possible_moves = self.get_moves(move.board_state)
    #     for move in possible_moves:
    #         moveKey =  move.board_state.split()[0] +" "+ move.board_state.split()[1]
    #         if moveKey in dataDict:
    #             print(dataDict[moveKey])
    #             self.getValueOfMove(move, 0, dataDict)
    #     return value

    def make_move(self, board_state, dataDict, opponent):
        possible_moves = self.get_moves(board_state)
        parent = str(self.game).split()[0] +" "+ str(self.game).split()[1]
        #movesValueDict = {}
        good_moves = {}
        if opponent != "MCTSAI":  
            for move in possible_moves:
                moveKey =  move.board_state.split()[0] +" "+ move.board_state.split()[1]
                if moveKey in dataDict:
                    if move.board_state.split()[1] == "w":
                        try:
                            losses = float(dataDict[moveKey][0])
                            wins = float(dataDict[moveKey][1])
                            ties = float(dataDict[moveKey][2])
                            score =  wins + losses + ties
                            totalGames = wins + abs(losses) + ties/0.001
                            score = score/totalGames
                            if score < 0.5 and len(possible_moves) >= 2:
                                possible_moves.remove(move)
                            else:
                                good_moves[move]=score
                        except:
                            doesNotExist = True
                    if move.board_state.split()[1] == "b":
                        try:
                            losses = float(dataDict[moveKey][1])
                            wins = float(dataDict[moveKey][0])
                            ties = float(dataDict[moveKey][2])
                            score =  abs(losses) - wins - ties
                            totalGames = wins + abs(losses) + ties/0.001
                            score = score/totalGames
                            if score < 0.5 and len(possible_moves) >= 2:
                                possible_moves.remove(move)
                            else:
                                good_moves[move]=score
                        except:
                            doesNotExist = True

        if good_moves:
            maximum = max(good_moves, key=good_moves.get)
            best_move = maximum
        else:
            best_move = random.choice(possible_moves)
        child = best_move.board_state.split()[0] +" "+ best_move.board_state.split()[1]
        try:
            if child not in dataDict[parent]:
                dataDict[parent].append(child)
                dataDict.update({child: [0,0,0]})
        except:
            #playing against player, don't save/update data
            playingAgainstPlayer = True
        
        return best_move.algebraic_move, dataDict

if __name__ == '__main__':
    #while True:
    test_engine = AIEngine('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #test_engine.prompt_user()
    test_engine.prompt_ai()


    # i = 0
    # while i < 100:
    #     test_engine = AIEngine('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #     test_engine.prompt_ai()
    #     i+=1
    # while True:
    #     test_engine = AIEngine('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #     test_engine.prompt_ai()

 # weight scores by the value of the pieces, king would be infinite
# calculate scores using min max, probably only want to use a depth of 2
# weight of pieces https://i.imgur.com/A7sntFs.png

# State 3 = stalemate
# State 2 = checkmate
# https://pastebin.com/VShyLen8
# https://pastebin.com/e8hQmx7Z

# index 0 is white wins
# index 1 is black wins
# index 2 is ties

# MCTS doesn't save any data when playing against a player