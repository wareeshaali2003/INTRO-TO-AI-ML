import sys

from math import inf
from crossword import *
from copy import deepcopy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var in self.variables:
            domain = self.domains[var]
            new_domain = []
            for value in domain:
                if len(value) == var.length:
                    new_domain.append(value)
            self.domains[var] = new_domain


    def revise(self, x, y):
        revised = False
        for i in range(len(self.domains[x])):
            x_val = self.domains[x][i]
            all_constraints = True
            for y_val in self.domains[y]:
                if self.constraints(x_val, y_val):
                    all_constraints = False
                    break
            if all_constraints:
                self.domains[x].remove(x_val)
                revised = True
        return revised

    def ac3(self, arcs=None):
        if arcs is None:
            arcs = []
            for x in self.variables:
                for y in self.neighbors[x]:
                    arcs.append((x, y))
            while arcs:
                x, y = arcs[0]
                arcs = arcs[1:]
                if self.revise(x, y):
                    if not self.domains[x]:
                        return False
                    for z in self.neighbors[x]:
                        if z != y:
                            arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        return set(assignment.keys()) == self.variables

    def consistent(self, assignment):
        for (x1, y1), (x2, y2) in self.overlaps:
            if (x1, y1) not in assignment or (x2, y2) not in assignment:
                continue
        if assignment[(x1, y1)] != assignment[(x2, y2)]:
            return False
        return True

    def order_domain_values(self, var, assignment):
         counts = {}
         for value in self.domains[var]:
             count = 0
         for neighbor in self.crossword.neighbors(var):
             if neighbor not in assignment:
                for neighbor_value in self.domains[neighbor]:
                    if not self.crossword.overlaps[var, neighbor]:
                        continue
                    if value[self.crossword.overlaps[var, neighbor][0]] != neighbor_value[self.crossword.overlaps[var, neighbor][1]]:
                        count += 1
         counts[value] = count
         return sorted(self.domains[var], key=lambda value: counts[value])

    def select_unassigned_variable(self, assignment):
        unassigned_vars = []
        for var in self.variables:
           if var not in assignment:
               unassigned_vars.append(var)
        if not unassigned_vars:
            return None
        min_domain_size = float('inf')
        selected_var = None
        for var in unassigned_vars:
            domain_size = len(self.domains[var])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                selected_var = var
            elif domain_size == min_domain_size and len(self.neighbors(var)) > len(self.neighbors(selected_var)):
                selected_var = var
        return selected_var
    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
            if result is not None:
                return result
        return None
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
