from typing import List, Tuple, Set

# Type aliases
Grid = List[List[int]]
Piece = List[List[int]]
Element = List[List[int]]
Patch = List[List[int]]
Integer = int
IntegerSet = Set[int]

# Functions with input and output as Grid
def rot90(grid: Grid) -> Grid:
    """Rotates the grid 90 degrees clockwise."""
    return [list(row) for row in zip(*grid[::-1])]

def rot180(grid: Grid) -> Grid:
    """Rotates the grid 180 degrees."""
    return [row[::-1] for row in grid[::-1]]

def rot270(grid: Grid) -> Grid:
    """Rotates the grid 270 degrees counterclockwise."""
    return [list(row) for row in zip(*grid)][::-1]

def trim(grid: Grid) -> Grid:
    """Trims the border of a grid."""
    rows = [row for row in grid if any(row)]
    if not rows:
        return []
    cols = list(zip(*rows))
    cols = [col for col in cols if any(col)]
    return [list(row) for row in zip(*cols)]

def tophalf(grid: Grid) -> Grid:
    """Returns the top half of the grid."""
    mid = len(grid) // 2
    return grid[:mid]

def bottomhalf(grid: Grid) -> Grid:
    """Returns the bottom half of the grid."""
    mid = len(grid) // 2
    return grid[mid:]

def lefthalf(grid: Grid) -> Grid:
    """Returns the left half of the grid."""
    mid = len(grid[0]) // 2
    return [row[:mid] for row in grid]

def righthalf(grid: Grid) -> Grid:
    """Returns the right half of the grid."""
    mid = len(grid[0]) // 2
    return [row[mid:] for row in grid]

def compress(grid: Grid) -> Grid:
    """Removes frontiers from the grid."""
    return trim(grid)

def cover(grid: Grid, patch: Patch) -> Grid:
    """Removes an object from the grid by covering it with the most common color."""
    # Assuming implementation fills grid cells with the most common color from the patch.
    most_common_color = max(set(sum(patch, [])), key=sum(patch, []).count)
    for r, row in enumerate(patch):
        for c, val in enumerate(row):
            if val != 0:  # Assuming 0 is the background
                grid[r][c] = most_common_color
    return grid

# Functions with input and output as Piece
def hmirror(piece: Piece) -> Piece:
    """Horizontally mirrors the piece."""
    return [row[::-1] for row in piece]

def vmirror(piece: Piece) -> Piece:
    """Vertically mirrors the piece."""
    return piece[::-1]

def dmirror(piece: Piece) -> Piece:
    """Diagonally mirrors the piece."""
    return [list(row) for row in zip(*piece)]

def cmirror(piece: Piece) -> Piece:
    """Mirrors the piece along the counterdiagonal."""
    return [list(row[::-1]) for row in zip(*piece[::-1])]

# Functions with input and output as Element
def palette(element: Element) -> IntegerSet:
    """Returns the set of colors present in the element."""
    return set(sum(element, []))

def recolor(value: Integer, patch: Patch) -> Element:
    """Recolors a patch to create an object."""
    return [[value if cell != 0 else 0 for cell in row] for row in patch]

