assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a,b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# This will concatenate the diagonal units, by list comprehension. The difference between the forward diagonal
# and the backwards diagonal is that we should traverse the columns in reverse order, from 9 to 1
diagonal_units = [[rows[x] + cols[x] for x in range(len(rows))]] + [[rows[x] + cols[-(x+1)] for x in range(len(rows))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
unitlist = row_units + column_units + square_units


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    #I guess this is not very pythonic
    #The algorithm works as follows:


    for unit in unitlist:
        # For each unit, we obtain the list of possible values that are bigger than 1 in that unit
        # In this list of possible values, we check boxes that have exactly 2 possibilites and if there
        # is another box with the same 2 possibilites, we assign it to a double_set variable that contains
        # the naked twins

        # If this double_set is not empty, we proceed to
        # eliminate all the chars from every naked twin in the boxes of the same unit
        list_of_values_in_unit = [values[box] for box in unit if len(values[box]) > 1]
        double_set = set([value for value in list_of_values_in_unit if (list_of_values_in_unit.count(value) >1 and len(value)==2)])
        if double_set:
            for item in double_set:
                for box in unit:
                    if len(values[box]) > 1 and values[box] != item:
                        values[box] = values[box].replace(item[0],'')
                    if len(values[box]) > 1 and values[box] != item:
                        values[box] = values[box].replace(item[1],'')
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Will traverse the peer list of a box to eliminate possible values when a box is solved
    Args:
        grid(string) - A grid in dictionary form.
    Returns:
        The modified grid by the assignment of a value to a box, using the assign_value function

    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Assigns a value to a box in the grid
    Args:
        grid(string) - A grid in dictionary form.
    Returns:
        The modified grid by the assignment of a value to a box, using the assign_value function

    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    """
    Applies the constraint strategies for a grid
    Args:
        grid(string) - A grid in dictionary form.
    Returns:
        The modified grid by the constraint propagation

    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Tries to solve the grid
    Args:
        grid(string) - A grid in dictionary form.
    Returns:
        The final grid, by consistently trying to reduce the puzzle

    """
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    #display(values)
    solution = search(values)

    if solution:
        return solution
    else:
        return None


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
