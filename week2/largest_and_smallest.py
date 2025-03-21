#the two other choices of checks made to check the output when there are 2 largest numbers and when all the numbers are the same
#and than there are 3 largest numbers and 3 smallest numbers
def largest_and_smallest(a,b,c): #choosing the largest number
    if a >= b and a >= c:
        largest_num = a
    elif b >= c:
        largest_num = b
    else:
        largest_num = c
    if a <= b and a <= c:  #choosing the smallest number
        smallest_num = a
    elif b <= c:
        smallest_num = b
    else:
        smallest_num = c
    return largest_num,smallest_num
def check_largest_and_smallest():
   a = (largest_and_smallest(17,1,6))
   b = (largest_and_smallest(1,17,6))
   c = (largest_and_smallest(1,1,2)) #when have 2 smallest number
   d = (largest_and_smallest(1,2,2)) #when have 2 largest numbers
   e = (largest_and_smallest(1,1,1)) #when have 3 largest numbers and 3 smallest numbers
   if a == (17,1) and b == (17,1) and c == (2,1) and d == (2,1) and e == (1,1) :
       return True
   else:
       return False

