import math
def circle_shape(): #calculates the shape of a circle with the radius
    r = float(input())
    return math.pi * r ** 2
def rectangle_shape(): #calculates the shape of a rectangle with width and length
    l = input()
    w = input()
    return float(l) * float(w)
def triangle_shape(): #calculates the shape of triangle with edges
    e = float(input())
    return e ** 2 * 3 ** 0.5 / 4
def shape_area():
    shape = float(input("Choose shape (1=circle, 2=rectangle, 3=triangle): "))
    if shape == 1:
        return(circle_shape())
    if shape == 2:
        return(rectangle_shape())
    if shape == 3:
        return(triangle_shape())
    if shape not in [1,2,3]:
        return
