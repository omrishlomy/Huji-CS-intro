def input_list():
    User_list = []
    Enter_loop = True
    sum_of_list = 0
    while Enter_loop:
        user_input = (input())
        if user_input != "": #adding the value to the list and to the summery of while is not empty
            user_input = float(user_input)
            User_list.append(user_input)
            sum_of_list += user_input
        if user_input == "":# add the summery to the list and end the loop
            User_list.append(sum_of_list)
            return User_list

def inner_product(vec_1,vec_2):
    if len(vec_1) == len(vec_2): #basic condition to start the multiplication
        inner_multiplication = 0
        if vec_1 == 0:
            return 0
        for i in range(len(vec_1)):
            inner_multiplication += vec_1[i] * vec_2[i]
        return inner_multiplication
    else:
        return

def sequence_monotonicity(sequence):
    monotonicity_up = 1
    monotonicity_very_up = 1
    monotonicity_down = 1
    monotonicity_very_down = 1
    for i in range(1, len(sequence)):# evaluates how many times a monotonic sequence is shown at the sequence
        if sequence[i-1] == sequence[i] or sequence[i-1] > sequence[i]:
            monotonicity_down += 1
        if sequence[i-1] == sequence[i] or sequence[i-1] < sequence[i]:
            monotonicity_up +=1
        if sequence[i - 1] < sequence[i]:
            monotonicity_very_up += 1
        if sequence[1 - 1] > sequence[i]:
            monotonicity_very_down += 1
    monotonicity_list = [monotonicity_up, monotonicity_very_up, monotonicity_down, monotonicity_very_down]
    max_monotonicity = len(sequence)
    for j in range(len(monotonicity_list)): # changes the int value to a boolean value according
        #to the lenght of the sequence
        if monotonicity_list[j] >= max_monotonicity:
            monotonicity_list[j] = True
        else:
            monotonicity_list[j] = False
    return monotonicity_list

def monotonicity_inverse(def_bool):
    True_num = 0
    False_num = 0
    for i in range(len(def_bool)):# summerize the numbers of True and False vakues at the list
        if def_bool[i] == True:
            True_num +=1
        else:
            False_num +=1
    if True_num >= 3:#its not possible to habe 3 or more True values
        return
    else:
        if True_num == 2:
            if def_bool[0] == True and def_bool[2] == True:
                num_list = [1, 1, 1, 1]
            if def_bool[1] == True and (def_bool[3] == True or def_bool[2] == True):
                return
            if def_bool[3] == True and (def_bool[0] == True or def_bool[1] == True):
                return
            if def_bool[1] == True and def_bool[0] == True:
                num_list = [1, 2, 3, 4]
            if def_bool[2] == True and def_bool[3] == True:
                num_list = [4, 3, 2, 1]
    if False_num == 3:#known also as True ==1
        if def_bool[0] == True:
            num_list = [1, 1, 2, 2]
        if def_bool[2] == True:
            num_list = [2, 2, 1, 1]
        else:
            return
    if False_num == 4: #this list is non monotonic of all kinds
            num_list = [1, 2, 1, 2]
    return num_list

def sum_of_3X3(i,j,mat): #calculate the sum of a sub matric of 3X3
    summery = 0
    for row in range(i, i+3):
        for column in range(j, j+3):
            summery += mat[row][column]
    return summery

def convolve(mat):
    New_Mat = []
    for i in range(len(mat)-2): #building the new matric accordind to number of rows and columns
        New_Mat.append([])
    for i in range(len(mat)-2): #adding the 3X3 matric's to the new matric
        for j in range((len(mat[i])-2)):
            summery = sum_of_3X3(i, j, mat)
            New_Mat[i].append(summery)
    return New_Mat

def sum_of_vectors(vec_list):
    sum_vec = []
    if len(vec_list) == 0:
        return
    for j in range(len(vec_list[0])):#run on the vector digits
        partial_sum = 0
        for i in range(len(vec_list)): #sum the j digit at all vectors
            partial_sum += vec_list[i][j]
        sum_vec.append(partial_sum)
    return sum_vec

def num_of_orthogonal(vectors):
    num_of_orth = 0
    small_vector_num =0
    for small_vector_num in range(len(vectors)):
        for big_vector_num in range(small_vector_num + 1, len(vectors)):
                if inner_product(vectors[small_vector_num], vectors[big_vector_num]) == 0:
                    num_of_orth += 1
    return num_of_orth











