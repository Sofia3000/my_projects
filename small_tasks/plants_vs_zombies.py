# check triangle
def get_winner(plants: list, zombies: list):
    # check parameters' types
    if not isinstance(plants, list) or not isinstance(zombies, list):
        raise TypeError('Arguments must be lists')
       
    # check elements in lists
    if not all(isinstance(item, int) for item in plants + zombies):
        raise TypeError('All elements in list must be integer numbers')

    # initial score variables
    plants_score = 0
    zombies_score = 0

    # lists length
    plants_len = len(plants)
    zombies_len = len(zombies)

    # compare length
    count = plants_len
    diff = count - zombies_len

    # lengths are not equal
    if diff > 0:
        plants_score += diff
        count = zombies_len
    elif diff < 0:
        zombies_score += abs(diff)

    # compare all pairs
    for p, z in zip(plants[:count], zombies[: count]):
        if p > z:
            plants_score += 1
        elif p < z:
            zombies_score += 1

    # score are equal
    if plants_score == zombies_score:
        # compare lists' powers
        return sum(plants) >= sum(zombies)

    # compare scores
    return plants_score > zombies_score
    
# test
assert get_winner([2,4,6,8], [1,3,5,7]) == True
assert get_winner([2,4], [1,3,5,7]) == False
assert get_winner([2,4,0,8], [1,3,5,7]) == True
assert get_winner([1,2,1,1], [2,1,1,1]) == True