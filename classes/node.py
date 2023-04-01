class Node:
    def __init__(self, parent, action, state_array, cost):
        self.parent = parent
        self.action = action
        self.position = state_array
        self.cost = cost

    def get_position(self):
        return self.position

    def get_action(self):
        return self.action

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_cost(self):
        return self.cost

    def __lt__(self, other):
        return self.cost < other.get_cost()

