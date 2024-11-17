def compare_grid(grid1, grid2):
    if len(grid1) != len(grid2):
        return False
    
    for row1, row2 in zip(grid1, grid2):
        if len(row1) != len(row2) or any(elem1 != elem2 for elem1, elem2 in zip(row1, row2)):
            return False
    
    return True