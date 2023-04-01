import heapq  # dla utrzymania fringe
from classes import node, minesweeper, system


class BFS:
    window: system.Window
    agent: minesweeper.Minesweeper
    node: node.Node

    def __init__(self, agent, window):
        self.agent = agent
        self.window = window

    def successor(self, current_position):
        new_nodes = []
        neighbours_list = self.agent.sensor(current_position[0], current_position[1])

        if current_position[2] == 180:  # jesli patrzy na polnoc
            if neighbours_list[0][1] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                if neighbours_list[0][1] == 'slowfloor':
                    cost = 3
                elif neighbours_list[0][1] == 'floor':
                    cost = 2
                elif neighbours_list[0][1] == 'encounter':
                    cost = 0
                tmp = ('forward', [current_position[0], current_position[1] - 1, 180], cost)
                new_nodes.append(tmp)
            if neighbours_list[1][0] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[1][0] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[1][0] == 'floor':
                #     cost = 2
                # elif neighbours_list[1][0] == 'encounter':
                #     cost = 0
                tmp = ('left', [current_position[0], current_position[1], 270], 1)
                new_nodes.append(tmp)
            if neighbours_list[1][2] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[1][2] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[1][2] == 'floor':
                #     cost = 2
                # elif neighbours_list[1][2] == 'encounter':
                #     cost = 0
                tmp = ('right', [current_position[0], current_position[1], 90], 1)
                new_nodes.append(tmp)

        if current_position[2] == 90:  # jesli patrzy na wschod
            if neighbours_list[1][2] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                if neighbours_list[1][2] == 'slowfloor':
                    cost = 3
                elif neighbours_list[1][2] == 'floor':
                    cost = 2
                elif neighbours_list[1][2] == 'encounter':
                    cost = 0
                tmp = ('forward', [current_position[0] + 1, current_position[1], 90], cost)
                new_nodes.append(tmp)
            if neighbours_list[0][1] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[0][1] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[0][1] == 'floor':
                #     cost = 2
                # elif neighbours_list[0][1] == 'encounter':
                #     cost = 0
                tmp = ('left', [current_position[0], current_position[1], 180], 1)
                new_nodes.append(tmp)
            if neighbours_list[2][1] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[2][1] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[2][1] == 'floor':
                #     cost = 2
                # elif neighbours_list[2][1] == 'encounter':
                #     cost = 0
                tmp = ('right', [current_position[0], current_position[1], 0], 1)
                new_nodes.append(tmp)

        if current_position[2] == 0:  # jesli patczy na poludzie
            if neighbours_list[2][1] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                if neighbours_list[2][1] == 'slowfloor':
                    cost = 3
                elif neighbours_list[2][1] == 'floor':
                    cost = 2
                elif neighbours_list[2][1] == 'encounter':
                    cost = 0
                tmp = ('forward', [current_position[0], current_position[1] + 1, 0], cost)
                new_nodes.append(tmp)
            if neighbours_list[1][2] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[1][2] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[1][2] == 'floor':
                #     cost = 2
                # elif neighbours_list[1][2] == 'encounter':
                #     cost = 0
                tmp = ('left', [current_position[0], current_position[1], 90], 1)
                new_nodes.append(tmp)
            if neighbours_list[1][0] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[1][0] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[1][0] == 'floor':
                #     cost = 2
                # elif neighbours_list[1][0] == 'encounter':
                #     cost = 0
                tmp = ('right', [current_position[0], current_position[1], 270], 1)
                new_nodes.append(tmp)

        if current_position[2] == 270:  # jesli patczy na wschod
            if neighbours_list[1][0] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                if neighbours_list[1][0] == 'slowfloor':
                    cost = 3
                elif neighbours_list[1][0] == 'floor':
                    cost = 2
                elif neighbours_list[1][0] == 'encounter':
                    cost = 0
                tmp = ('forward', [current_position[0] - 1, current_position[1], 270], cost)
                new_nodes.append(tmp)
            if neighbours_list[2][1] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[2][1] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[2][1] == 'floor':
                #     cost = 2
                # elif neighbours_list[2][1] == 'encounter':
                #     cost = 0
                tmp = ('left', [current_position[0], current_position[1], 0], 1)
                new_nodes.append(tmp)
            if neighbours_list[0][1] not in ['wall', 'cliff_south', 'cliff_east', 'cliff_north', 'cliff_west']:
                # if neighbours_list[0][1] == 'slowfloor':
                #     cost = 10
                # elif neighbours_list[0][1] == 'floor':
                #     cost = 2
                # elif neighbours_list[0][1] == 'encounter':
                #     cost = 0
                tmp = ('right', [current_position[0], current_position[1], 180], 1)
                new_nodes.append(tmp)

        return new_nodes

    # fringe = struktura danych przeszowyjąca wierchowki do odwiedzenia
    # explored = lista odwiedzonych stanow
    # position_at_beginning = stan poczatkowy
    # succ = funkcja nastempnika
    # goaltest = test spewnienia celu

    def graphsearch(self, fringe, explored, succ, goaltest):

        def manhattan(state, target_state):
            return abs(state[0] - target_state[0]) + abs(state[1] - target_state[1])

        self.window.pause(True)

        position_at_beginning = [self.agent.position_x, self.agent.position_y,
                                 self.agent.rotation_degrees]  # x, y, gdzie_patczy
        final_action_list = []  # lista co ma robic zeby dojechac do miny
        root = node.Node(None, None, position_at_beginning, 2)  # parent, action, position, cost

        heapq.heappush(fringe, (0, root))  # add first node to fringe

        while len(fringe) != 0:  # poki sa wezly do odwiedzenia(na fringe)

            if len(fringe) == 0:
                return False

            # get node from fringe
            tmp_node = heapq.heappop(fringe)  # tuple(priority, node)
            tmp_node_position = tmp_node[1].get_position()  # x, y , gdzie patczy

            # jesli tmp node to goaltest
            if tmp_node_position[:2] == goaltest:
                print('Find\n')

                while tmp_node[1].get_parent() is not None:
                    final_action_list.append(tmp_node[1].get_action())
                    tmp_node = tmp_node[1].get_parent()
                final_action_list.reverse()
                # print(final_action_list)
                self.window.pause(False)
                return final_action_list

            explored.append(tmp_node[1])  # add node to array of visited nodes

            neighbours_list_of_our_node = self.successor(tmp_node_position)  # lista możliwych akcij
            # print(neighbours_list_of_our_node)

            for node_ in neighbours_list_of_our_node:
                # node_ is tuple(action, [x, y, gdzie_patczy], cost)

                notInFringe = True  # false if node in fringe
                notInExplored = True  # false if node in explored

                p = manhattan(node_[1], goaltest) + node_[2]
                # wyznacza jaki jest priorytet nastempnika
                # manchaten from node_ + cost of way from tmp_ode to node_

                priority_in_fringe = 0
                counter = 0
                index_of_node_in_fringe = 0  # zero if node not in fringe

                for fringeNode in fringe:  # isc po wszystkich wezlach ktore juz sa w fringe
                    # jesli nasz wezel juz jest w fringe
                    if fringeNode[1].get_position()[0] == node_[1][0] and fringeNode[1].get_position()[1] == node_[1][
                        1] and fringeNode[1].get_position()[2] == node_[1][2]:
                        notInFringe = False
                        priority_in_fringe = fringeNode[0]
                        # number of element in fringe
                        index_of_node_in_fringe = counter
                    counter = counter + 1

                for exploredNode in explored:  # isc po wszystkich wezlach z listy explored
                    # jesli nasz wezel juz jest w explored
                    if exploredNode.get_position()[0] == node_[1][0] and exploredNode.get_position()[1] == node_[1][
                        1] and exploredNode.get_position()[2] == node_[1][2]:
                        notInExplored = False

                # if node not in fringe and not in explored
                if notInFringe and notInExplored:
                    x = node.Node(tmp_node, node_[0], node_[1], node_[2])  # parent, action, state_array, cost
                    heapq.heappush(fringe, (p, x))
                # if node not in fringe
                elif notInFringe is False and (priority_in_fringe > p):
                    x = node.Node(tmp_node, node_[0], node_[1], node_[2])  # parent, action, state_array, cost
                    tmp = list(fringe[index_of_node_in_fringe])
                    tmp[0] = p
                    tmp[1] = x
                    fringe[index_of_node_in_fringe] = tuple(tmp)
                self.window.draw_search([self.agent.position_x, self.agent.position_y], [node_[1][0], node_[1][1]],
                                        self.agent.current_map.tile_size, self.agent.current_map, self.agent)
