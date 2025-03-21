import math
def quadratic_equation(a,b,c):
    if a == b == c == 0 : #when there are infine solutions
        return "x1,x2"
    if a != 0 :
        numerator = (b ** 2 -4 * a * c)
        x1 = (-b + numerator ** 0.5 ) / 2 * a
        x2 = (-b - numerator ** 0.5) / 2 * a
    else :
        if b !=0: #the solution of a linear equation
            x1 = -c/b
            x2 = None
        else:
            x1 = None
            x2 = None
    if isinstance(x1, float): #check if x1 is a solution
        solution1 = x1
    else:
        solution1 = None
    if isinstance(x2, float): #check if x2 is a solution
        solution2 =  x2
    else:
        solution2 = None
    return(solution1, solution2)
def quadratic_equation_user_input():
    a,b,c = input("Insert coefficients a, b, and c: ").split()
    a = float(a)
    b = float(b)
    c = float(c)
    if a == 0 :
        print("The parameter 'a' may not equal 0")
        return
    solution1, solution2 = quadratic_equation(a,b,c)
    if solution1 != None and solution2 != None : #when 2 solutions
        if solution2 != solution1:
            print("The equation has 2 solutions: " + str(solution1) + " and " + str(solution2))
        elif solution2 == solution1: #when 1 solution and a!=0
            print("The equation has 1 solution: " + str(solution2))
    if solution1 == None and solution2 == None : #no solutions
        print("The equation has no solutions")
    if solution1 ==None and solution2 != None: # 1 solution
        print("The equation has 1 solution:" + str(solution2))
    if solution2 == None and solution1 != None: # 1solution
        print("The equation has 1 solution:" + str(solution1))

print(quadratic_equation(14,-49,21))









