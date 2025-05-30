# check triangle
def check_triangle(sides: list):
    # check type
    if not isinstance(sides, list):
        raise TypeError('Argument must be a list')
    
    # check list length
    count = len(sides)
    if count != 3:
        raise ValueError('List must consist of three elements')
        
    # check parameters' types
    if not all(isinstance(side, int) for side in sides):
        raise TypeError('All elements in list must be integer numbers')

    # check parameters' types
    if not all(side >= 0 for side in sides):
        raise ValueError('All elements in list must be positive numbers')
    
    # calculate perimeter
    perimeter = sum(sides)
    
    # check all sides
    for side in sides:
        # side has wrong length
        if perimeter - side <= side:
            return False
    
    return True
    
# test
assert check_triangle([5, 3, 4]) == True
assert check_triangle([6, 8, 10]) == True
assert check_triangle([100, 3, 65]) == False
