from fishing_game_core.player_utils import *
from fishing_game_core.shared import *
from fishing_game_core.game_tree import *
from collections import defaultdict
import time
import random
random.seed(2022)
import sys
import math



class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return

class MinimaxSearchModel(object):

    def __init__(self, initial_data):
        self.hash_save0 = defaultdict(lambda : -1)
        self.hash_save1 = defaultdict(lambda : -1)
        self.initial_table = self.gen_zobrist_table(initial_data)

    # def ordering_children(self, children, isreverse):
    #     if isreverse:
    #         reverse_children = sorted(children, key=lambda child: self.heuristic(child.state), reverse=True)
    #         return reverse_children        
    #     else:
    #         sorted_children = sorted(children, key=lambda child: self.heuristic(child.state), reverse=True)
    #         return sorted_children
    
    def gen_zobrist_table(self, initial_data):
        fish_and_ply = len(initial_data) + 2
        table = [[[0 for i in range(fish_and_ply)] for j in range(20)] for k in range(20)]
        for i in range(20):
            for j in range(20):
                for k in range(fish_and_ply):
                    table[i][j][k] = random.getrandbits(64)
        return table

    def get_hash(self, state, table):
        fish_positions = state.get_fish_positions()
        hook_positions = state.get_hook_positions()
        ply0_pos = len(table[0][0]) - 2
        ply1_pos = len(table[0][0]) - 1
        h = 0
        for pos in fish_positions:
            h = h ^ table[fish_positions[pos][0]][fish_positions[pos][1]][pos]
        h = h ^ table[hook_positions[0][0]][hook_positions[0][1]][ply0_pos]
        h = h ^ table[hook_positions[1][0]][hook_positions[1][1]][ply1_pos]
        return h

    def heuristic(self, node):
        fish_scores = node.state.fish_scores
        hook_positions = node.state.hook_positions
        fish_positions = node.state.fish_positions
        score_max, score_min = node.state.get_player_scores()
        x1 , y1 = hook_positions[0]
        x2 , y2 = hook_positions[1]
        weighted_score = 0
        for fish_id in fish_positions:
            x0 , y0 = fish_positions[fish_id]
            dist_max = abs(x0 - x1)
            dist_min = abs(x0 - x2)            
            if x1 < x2 & x2 < x0:
                dist_max = 20 - dist_max
            elif x0 < x2 & x2 < x1:
                dist_max = 20 - dist_max
            elif x0 < x1 & x1 < x2:
                dist_min = 20 - dist_min
            elif x2 < x1 & x1 < x0:
                dist_min = 20 - dist_min
            
            l_max = dist_max + abs(y0 - y1) + 19 -y0 + 1
            l_min = dist_min + abs(y0 - y2) + 19 -y0 + 1
            
            weighted_score += fish_scores[fish_id] * (1/l_max - 1/l_min)

        return weighted_score + score_max - score_min

    def get_best_move(self, node, max_depth, time_allowed):
        self.start_time = time.time()
        self.time_limit = time_allowed
        children = node.compute_and_get_children()

        if len(children) == 1:
            return children[0].move
        else:
            for depth in range(1, max_depth):
                alpha, beta = float('-inf'), float('inf')
                move = 0
                movelist=[]
                best_p = alpha
                children_p = [alpha] * len(children)
                for i, j in enumerate(children):
                    p = self.alpha_beta_zob(j, alpha, beta, 1, depth, 1)
                    children_p[i] = p
                    if best_p < p:
                        best_p = p
                        move = j.move
                        movelist.append(move)
                        alpha = p
                        if time.time() - self.start_time > self.time_limit:
                            return move
                for i in range(len(children)):
                    for j in range(i + 1, len(children)):
                        if children_p[i] < children_p[j]:
                            children_p[i], children_p[j] = children_p[j], children_p[i]
                            children[i], children[j] = children[j], children[i]
            move_len = len(movelist)
            if move_len>=3 and (movelist[-1] == movelist[-2] == movelist[-3] == 0):
                move = random.choice([1, 2, 3, 4])
            return move

    def alpha_beta_zob(self, node, alpha, beta, depth, max_depth, player):
        if depth == max_depth:
            return self.heuristic(node)

        else:
            children = node.compute_and_get_children()
            if len(children) == 0:
                return self.heuristic(node)
            h = self.get_hash(node.state, self.initial_table)
            explored_depth = max_depth - depth
            if player == 0:
                representative = self.hash_save0[h]
            else:
                representative = self.hash_save1[h]
            if representative != -1:
                if representative.explored_depth >= explored_depth:
                    if representative.value == math.inf:
                        return representative.value
         
            if node.state.player == 0:
                best_value = float('-inf')
                best_move=0
                sorted_children = sorted(children, key=lambda child: self.heuristic(child), reverse=True)
                for child in sorted_children:
                    v = self.alpha_beta_zob(child, alpha, beta, depth + 1, max_depth, 1-player)
                    if v > best_value:
                        best_value = v
                        best_move = child.move
                        alpha = max(alpha, best_value)
                    if alpha >= beta:
                        break
                    if time.time() - self.start_time > self.time_limit:
                        break
            else:
                best_value = float('inf')
                best_move=0
                sorted_children = sorted(children, key=lambda child: self.heuristic(child), reverse=False)
                for child in sorted_children:
                    v = self.alpha_beta_zob(child, alpha, beta, depth + 1, max_depth, 1-player)
                    if v < best_value:
                        best_value = v
                        best_move = child.move
                        beta = min(beta, best_value)
                    if alpha >= beta:
                        break
                    if time.time() - self.start_time > self.time_limit:
                        break

            if representative != -1:
                if explored_depth > representative.explored_depth:
                    representative.explored_depth = explored_depth
                    representative.value = best_value
                    representative.best_move = best_move
            elif explored_depth > 1:
                new_representative = StateSave(explored_depth, best_value, best_move)
                if player == 0:
                    self.hash_save0[h] = new_representative
                else:
                    self.hash_save1[h] = new_representative
            
            return best_value



class PlayerControllerMinimax(PlayerController):
  
    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def gen_zobrist_table(self, initial_data):
        fish_ply = len(initial_data) + 2
        table = [[[0 for i in range(fish_ply)] for j in range(20)] for k in range(20)]
        for i in range(20):
            for j in range(20):
                for k in range(fish_ply):
                    table[i][j][k] = random.getrandbits(64)
        return table

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)
            start = time.time()
            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(model=model, initial_tree_node=node)
            end = time.time()
            # Execute next action
            self.sender({"action": best_move, "search_time": end-start})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model 
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3}, 
          'fish1': {'score': 2, 'type': 1}, 
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        
        initial_table = MinimaxSearchModel(initial_data)

        return initial_table

    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node 
        :type initial_tree_node: game_tree.Node 
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE FROM MINIMAX MODEL ###
        
        # NOTE: Don't forget to initialize the children of the current node 
        #       with its compute_and_get_children() method!
        next_move = model.get_best_move(initial_tree_node, 9, 0.054)
        #random_move = random.randrange(5)
        #return ACTION_TO_STR[random_move]
        return ACTION_TO_STR[next_move]

class StateSave(object):

    def __init__(self, explored_depth, value, best_move):
        #self.node = node
        self.explored_depth = explored_depth
        self.value = value
        self.best_move = best_move