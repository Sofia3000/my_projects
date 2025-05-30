import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # all cells are mines
        if self.count == len(self.cells):
            return self.cells
        # no cells that are definitely mines
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # all cells are safe
        if self.count == 0:
            return self.cells
        # no cells that are definitely safe
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # check if cell is in cells
        if cell in self.cells:
            # delete cell
            self.cells.remove(cell)
            # check count
            if self.count > 0:
                # decrease count
                self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # check if cell is in cells
        if cell in self.cells:
            # delete cell
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark the cell as a move
        self.moves_made.add(cell)
        # mark the cell as safe
        self.mark_safe(cell)

        # add a new sentence
        # set for cells
        neighbor_cells = []
        # check all neighbors
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                # check if indexes is in bound
                if 0 <= i < self.height and 0 <= j < self.width:
                    # check if current cell is not marked
                    if (i, j) not in self.safes and (i, j) not in self.mines:
                        # add cell to cells in sentences
                        neighbor_cells.append((i, j))
                    # decrease count if we delete cell that is mine
                    if (i, j) in self.mines:
                        count -= 1
        # add new sentence to knowledge if it is not there
        new_sentence = Sentence(neighbor_cells, count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # add new knowledges
        while True:
            # generate new sentences
            for i in range(len(self.knowledge)):
                n = len(self.knowledge)
                for j in range(i+1, n):
                    diff = None
                    count = 0
                    # self.knowledge[i].cells is subset of self.knowledge[j].cells
                    if self.knowledge[i].cells < self.knowledge[j].cells:
                        # get new set of cells
                        diff = self.knowledge[j].cells - self.knowledge[i].cells
                        # get new count
                        count = self.knowledge[j].count - self.knowledge[i].count
                    # self.knowledge[j].cells is subset of self.knowledge[i].cells
                    elif self.knowledge[j].cells < self.knowledge[i].cells:
                        # get new set of cells
                        diff = self.knowledge[i].cells - self.knowledge[j].cells
                        # get new count
                        count = self.knowledge[i].count - self.knowledge[j].count
                    # miss this sets
                    else:
                        continue
                    # create new sentence if diff is not empty
                    if diff:
                        tmp = Sentence(list(diff), count)
                        # add new sencence to database
                        if tmp not in self.knowledge:
                            self.knowledge.append(tmp)

            # mark additional cells as safe or as mines
            # safe cells
            safe_cells = set()
            # mines
            mine_cells = set()
            # get marked cells from knowledge
            for sentence in self.knowledge:
                safe_cells |= sentence.known_safes()
                mine_cells |= sentence.known_mines()
            # stop if we can not mark new cells
            if not safe_cells and not mine_cells:
                break
            # convert sets to lists
            safe_cells = list(safe_cells)
            mine_cells = list(mine_cells)
            # mark safe cells
            for c in safe_cells:
                self.mark_safe(c)
            # mark mines
            for c in mine_cells:
                self.mark_mine(c)

            # delete empty sentences from database
            i = 0
            while i < len(self.knowledge):
                # sentence is empty
                if not self.knowledge[i].cells:
                    # delete the sencence
                    del self.knowledge[i]
                else:
                    i += 1

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # all safe cells that are available
        safe_cells = self.safes - self.moves_made        
        # if safe_cells is empty
        if not safe_cells:
            # no safe cells
            return None
        # return random safe cell
        return safe_cells.pop()

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # all cells that are available
        cells = set()
        for i in range(self.height):
            for j in range(self.width):
                cells.add((i, j))
        # delete cells that are mines or opened
        cells = cells - self.mines - self.moves_made
        # if cells is empty
        if not cells:
            # no available cells
            return None
        # return random cell
        return cells.pop()
