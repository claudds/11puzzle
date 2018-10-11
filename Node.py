###################################
## Claudia Della Serra, 26766048 ##
###################################

class Node:
    move_priority = ["UP", "UP-RIGHT", "RIGHT", "DOWN-RIGHT", "DOWN", "DOWN-LEFT", "LEFT", "UP-LEFT"]

    def __init__(self, value, parent=None, level=None):
        self.value = value
        self.parent = parent
        self.level = level
        # The cost in this case can represent both h(n) or f(n) depending on which algorithm is being used.
        self.cost = None

    def set_cost(self, estimate):
        self.cost = estimate

    def get_cost(self):
        return self.cost

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def get_level(self):
        return self.level

    def derive_children(self, level):
        if self.value == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0] :
            return None

        self.children = []
        empty_space = self.value.index(0)

        child1 = self.slide("UP", empty_space, self.level+1)
        child2 = self.slide("UP-RIGHT", empty_space, self.level+1)
        child3 = self.slide("RIGHT", empty_space, self.level+1)
        child4 = self.slide("DOWN-RIGHT", empty_space, self.level+1)
        child5 = self.slide("DOWN", empty_space, self.level+1)
        child6 = self.slide("DOWN-LEFT", empty_space, self.level+1)
        child7 = self.slide("LEFT", empty_space, self.level+1)
        child8 = self.slide("UP-LEFT", empty_space, self.level+1)

        self.children.extend([child1, child2, child3, child4, child5, child6, child7, child8])
        self.children = list(filter(None, self.children))

    def slide(self, direction, empty, level):
        child = self.value.copy()
        direction_index = self.move_priority.index(direction)

        puzzle_width = 4
        puzzle_height = 3
        jump = 0

        if direction_index == 0: #UP
            if empty not in range(0, puzzle_width):
                jump = puzzle_width
                child[empty], child[empty-jump] = child[empty-jump], child[empty]
                return Node(child, self, level)
            else : return None
        if direction_index == 1: #UP-RIGHT
            if empty not in range(0, puzzle_width) and (empty+1) % puzzle_width != 0:
                jump = puzzle_width-1
                child[empty], child[empty-jump] = child[empty-jump], child[empty]
                return Node(child, self, level)
            else: return None
        if direction_index == 2: #RIGHT
            if (empty+1) % puzzle_width != 0:
                child[empty], child[empty+1] = child[empty+1], child[empty]
                return Node(child, self, level)
            else: return None
        if direction_index == 3: #DOWN-RIGHT
            if empty not in range(((puzzle_height*puzzle_width)-puzzle_width), (puzzle_height*puzzle_width)) and \
                    (empty+1) % puzzle_width != 0:
                jump = 1+puzzle_width
                child[empty], child[empty+jump] = child[empty+jump], child[empty]
                return Node(child, self, level)
            else: return None
        if direction_index == 4: #DOWN
            if empty not in range(((puzzle_height*puzzle_width)-puzzle_width), (puzzle_height*puzzle_width)):
                jump = puzzle_width
                child[empty], child[empty+jump] = child[empty+jump], child[empty]
                return Node(child, self, self.level+1)
            else: return None
        if direction_index == 5: #DOWN-LEFT
            if empty not in range(((puzzle_height*puzzle_width)-puzzle_width), (puzzle_height*puzzle_width)) and \
                    empty % puzzle_width != 0:
                jump = puzzle_width-1
                child[empty], child[empty+jump] = child[empty+jump], child[empty]
                return Node(child, self, self.level+1)
            else: return None;
        if direction_index == 6: #LEFT
            if empty % puzzle_width != 0 :
                child[empty], child[empty-1] = child[empty-1], child[empty]
                return Node(child, self, self.level+1)
            else: return None
        if direction_index == 7: #UP-LEFT
            if empty not in range(0, puzzle_width) and empty % puzzle_width != 0:
                jump = puzzle_width+1
                child[empty], child[empty-jump] = child[empty-jump], child[empty]
                return Node(child, self, self.level+1)
            else:
                return None

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self, other):
        return self.cost <= other.cost
