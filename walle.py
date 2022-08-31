import numpy as np

class WallE:

    def __init__(self, matrix):
        self.grid = matrix
        self.current_index = None
        self.previous_index = None
        self.num_plants_collected = 0
        self.is_finished = False

    def get_center_indices(self):
        m, n = self.grid.shape
        # The case where number of columns and rows are both divisible by 2
        if m % 2 == 0 and n % 2 == 0:
            m, n = (m // 2)-1, (n // 2)-1
            max_val = self.grid[m, n]
            start_idx = (m, n)
            # These are the potential starting point positions
            combos = [(m + 1, n), (m, n + 1), (m + 1, n + 1)]

            # This will update the starting index if one of the positions has a higher value
            for r, c in combos:
                if self.grid[r, c] > max_val:
                    max_val = self.grid[r, c]
                    start_idx = (r, c)

        # The case where number of columns and rows are both not divisible by 2
        elif m % 2 != 0 and n % 2 != 0:
            # Int casting will round up to the middle row/col
            start_idx = (int(m / 2), int(n / 2))

        # Case where number of rows are even, but number of columns is odd
        elif m % 2 == 0 and n % 2 != 0:
            m, n = (m // 2) - 1, int(n / 2)
            max_val = self.grid[m, n]
            start_idx = (m, n)
            if self.grid[m + 1, n] > max_val:
                start_idx = (m + 1, n)

        # Case where num rows are odd, but num cols is even
        else:
            m, n = int(m / 2), n // 2
            max_val = self.grid[m, n]
            start_idx = (m, n)
            if self.grid[m + 1, n] > max_val:
                start_idx = (m + 1, n)
        self.current_index = start_idx
        x, y = start_idx
        self.num_plants_collected += self.grid[x, y]
        self.grid[x, y] = 0
        return start_idx

    def find_next_cell(self):
        x, y = self.current_index
        max_val = 0
        temp_next_idx = None
        combos = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

        # This will help dictate which cells wall-e can move to (checking for edges to determine possible moves)
        if x == 0 and y==0:
            combos = [(x + 1, y), (x, y + 1)]

        # These need to come first since they are more complex conditionals
        # (i.e dont want to hit y==0 only if y==0 and x ==3)
        elif x == 0 and y == self.grid.shape[1] - 1:
            combos = [(x + 1, y), (x, y - 1)]
        elif x == self.grid.shape[0] - 1 and y == 0:
            combos = [(x, y + 1), (x - 1, y)]
        elif x==0:
            combos = [(x + 1, y), (x, y + 1), (x, y - 1)]
        elif y==0:
            combos = [(x + 1, y), (x, y + 1), (x - 1, y)]
        elif y==self.grid.shape[1] - 1:
            combos = [(x + 1, y), (x, y - 1), (x - 1, y)]
        elif x == self.grid.shape[0] - 1:
            combos = [(x - 1, y), (x, y + 1), (x, y - 1)]


        # Search the values from the cell locations in combos, and update if needed
        for r, c in combos:
            cell_val = self.grid[r, c]
            if cell_val > max_val:
                max_val = cell_val
                temp_next_idx = (r, c)

        # If temp_next_idx is still None, wall-e has no moves left to make so return the num of plants he collected
        if temp_next_idx is not None:
            # Prev index is simply for me to track the previous move while debugging
            self.previous_index = self.current_index
            self.current_index = temp_next_idx
            r,c = self.current_index

            #Update num plants collected
            self.num_plants_collected += self.grid[r, c]
            self.grid[r, c] = 0
        else:
            self.is_finished = True

    # This method is used to move across the grid and collect plants
    def explore(self):
        #Get the starting indices
        self.get_center_indices()

        # Keep exploring until there are no moves left to take
        while not self.is_finished:
            self.find_next_cell()
        print(self.num_plants_collected)
        return self.num_plants_collected


# Example  5x5 matrix
# grid = np.array([[1, 4, 3, 2, 9],
#     [0, 0, 6, 0, 7],
#     [8, 9, 1, 0, 9],
#     [3, 1, 0, 5, 8],
#     [0, 7, 1, 0, 5]])

# Example 4x5 matrix
grid = np.array([[1, 4, 3, 2, 9],
    [0, 0, 6, 0, 7],
    [8, 9, 1, 0, 9],
    [3, 1, 0, 5, 8]])

# Example with a 4x4 matrix
# grid = np.array([[1, 4, 3, 2],
#     [0, 0, 6, 0],
#     [8, 9, 1, 0],
#     [3, 1, 0, 5]])


walle = WallE(grid)

walle.explore()
