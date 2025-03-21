#NAME : Omri Shlomy
#ID : 208394718
#exercise 7 course intro

from ex7_helper import *


def mult(x,y):
    if x ==0:
        return 0
    elif x >0:
        return add(y,mult(y,subtract_1(x))) #add the number y to the n-1 iteration

def is_even(n):
    if n == 0:
        return True
    if n < 0:
        return False
    else:
        return is_even(subtract_1(subtract_1(n)))


def log_mult(x,y):
    if y <= 0:
        return 0
    if not is_odd(y):
        return add(log_mult(x,divide_by_2(y)),log_mult(x,divide_by_2(y)))
    if is_odd(y):
        return add(x,add(log_mult(x,divide_by_2(y)),log_mult(x,divide_by_2(y))))


def is_power(b,x):
    if b==1 and x !=1:
        return False
    else:
        return is_power_temp(b,x,b)
def is_power_temp(b,x,t):
    if t == x:
        return True
    if t > x:
        return False
    if t < x:
        t = log_mult(b, t)
        return is_power_temp(b, x, t)


def reverse(s):
    if len(s)==1:
        return s
    else:
        return append_to_end(reverse(s[1:]), s[0])


def play_hanoi(hanoi, n, src, dest, temp):
    if n <= 0:
        return
    if n == 1:
        hanoi.move(src,dest)
    else:
        play_hanoi(hanoi,n-1,src,temp,dest)
        hanoi.move(src,dest)
        play_hanoi(hanoi,n-1,temp,dest,src)

def number_of_ones(n):
    if n == 1:
        return 1
    else:
        return is_1_in_num(n) + number_of_ones(n-1)


def is_1_in_num(n):
    count = 0
    if n == 1:
        count += 1
    if n < 10:
        return count
    if n % 10 == 1:
        count += 1
    else:
        remaining_digits = n // 10
        return count + is_1_in_num(remaining_digits)

def compare_2d_lists(l1,l2):
    return helper_compare(l1,l2,0,0)


def helper_compare(l1,l2,i,j):
    if len(l1) <= i and len(l2) <= i:
        return True
    elif len(l1) > i and len(l2) > i:
        if len(l1[i]) <= j and len(l2[i]) <= j:
            return True
        elif len(l1[i]) > j and len(l2[i]) > j:
            if l1[i][j] != l2[i][j]:
                return False
            else:
                return helper_compare(l1, l2, i+1, j) and helper_compare(l1,l2,i,j+1)
        else:
            return False
    else:
        return False


def magic_list(n):
    lst = []
    if n == 0:
        return lst
    else:
        major_lst = magic_list(n-1)
        relative_lst = magic_list(n-1)
        major_lst.append(relative_lst)
    return major_lst






















