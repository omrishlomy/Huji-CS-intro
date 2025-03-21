from typing import List, Tuple, Set, Optional


# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]
def check_forward(picture,row,col,count,lst):
    """check the values from the cell and forward"""
    steps = 0
    for row in range(row+1,len(picture)):
        steps += 1
        if picture[row][col] in lst:
            count +=1
        else:
            break
    row = row - steps
    for col in range(col+1,len(picture[row])):
        if picture[row][col] in lst:
            count +=1
        else:
            break
    return count
def check_backward(picture,row,col,count,lst):
    """checks the values from the cel and backwards"""
    steps = 0
    for row in range(row-1,-1,-1):
        steps += 1
        if picture[row][col] in lst or picture[row][col] in lst:
            count +=1
        else:
            break
    row = row + steps
    for col in range(col-1,-1,-1):
        if picture[row][col] in lst or picture[row][col] in lst:
            count +=1
        else:
            break
    return count



def check_around(picture, row,col,lst):
    """check the values of the cells around location"""
    count = 1
    count = check_forward(picture,row, col,count,lst)
    count = check_backward(picture,row, col,count,lst)
    return count



def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """checks the values around a cell while consider a unknown cell as a white cell"""
    lst_for_count = [1, -1]
    if picture[row][col] not in lst_for_count:
        return 0
    else:
        return check_around(picture, row, col,lst_for_count)




def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """checks the values around a cell while consider a unknown cell as a black cell"""
    lst_for_count = [1]
    if picture[row][col] not in lst_for_count:
        return 0
    else:
        return check_around(picture, row, col,lst_for_count)



def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    """checks if a picture contains the constrains"""
    constrain = 1
    for loc in constraints_set:
        row = loc[0]
        col = loc[1]
        count_max = max_seen_cells(picture,row,col)
        count_min = min_seen_cells(picture,row,col)
        if loc[2] > count_max or loc[2] < count_min:
            return 0
        if loc[2] == count_min == count_max:
            continue
        if count_min < loc[2] <= count_max:
            constrain += 1
    if constrain > 1:
        return 2
    elif not is_not_full(picture):
        return 1
    else:
        return 2

def is_not_full(picture):
    """check if -1 is in the picture"""
    for row in range(len(picture)):
        if -1 in picture[row]:
            return True
    return False


def is_full(picture):
    """fill black the rest of the board if a solution is already found"""
    for row in range(len(picture)):
        for col in range(len(picture[0])):
            if picture[row][col] == -1:
                picture[row][col] = 0
    return True



def helper_solve_puzzle(picture,constraints_set,index,n,m,count,find_all):
    if check_constraints(picture, constraints_set)==0:
        return False
    if check_constraints(picture, constraints_set) == 1 and index == n*m and is_full(picture):# found a solution
        if find_all:
            count[0] += 1
            return
        elif not find_all:
            return picture
    cell_loc = (index//m,index % m)
    picture[cell_loc[0]][cell_loc[1]] = 0
    sol = helper_solve_puzzle(picture, constraints_set, index + 1, n, m, count, find_all)
    if not sol:
        picture[cell_loc[0]][cell_loc[1]] = 1
        sol = helper_solve_puzzle(picture, constraints_set, index + 1, n, m, count, find_all)
        if not sol:
            picture[cell_loc[0]][cell_loc[1]] = -1
            return False
    return picture





def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    picture = [[-1] * m for _ in range(n)]
    num_solutions = helper_solve_puzzle(picture,constraints_set,0,n,m,[0],False)
    if num_solutions == False:
        return
    return num_solutions



def check_necessarity(set_constraints,picture):
    set_constraints = list(set_constraints)
    unnecessaries_lst = []
    for constrant in range(len(set_constraints)):
        constrant_check = set_constraints[constrant]
        set_constraints.remove(set_constraints[constrant])
        if solve_puzzle(set(set_constraints),len(picture),len(picture[0])) != None:
            unnecessaries_lst.append(constrant_check)
        set_constraints.append(constrant_check)
    if len(set_constraints) != len(unnecessaries_lst):
       set_constraints = set(set_constraints).difference(set(unnecessaries_lst))
    return set(set_constraints)

def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
        picture = [[-1] * m for _ in range(n)]
        count = [0]  # Initialize count as a list to make it mutable
        helper_solve_puzzle(picture, constraints_set, 0, n,m, count, True)
        return count[0]

def reduce_solutions(set_constrants,n,m):
    number_of_sol = how_many_solutions(set_constrants,n,m)
    removed_constraints = []
    while number_of_sol == 1:
        removed_constraints.append(set_constrants.pop())
        number_of_sol = how_many_solutions(set_constrants,n,m)
    set_constrants.add(removed_constraints[-1])
    return set_constrants


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    set_constrains = []
    lst = [1]
    for index in range(len(picture)* len(picture[0])):
        row = index // len(picture[0])
        col = index % len(picture[0])
        if picture[row][col] == 0:
            set_constrains.append((row,col,0))
        else:
            count = check_around(picture,row,col,lst)
            set_constrains.append((row,col,count))
    set_constrains = set(set_constrains)
    set_constrains = reduce_solutions(set_constrains,len(picture),len(picture[0]))
    set_constrains = check_necessarity(set_constrains,picture)
    return set_constrains








