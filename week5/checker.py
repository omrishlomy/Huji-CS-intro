import math
import ex5_helper


def separate_channels(image):
    image_lst = []
    for channel in range(len(image[0][0])):
        image_lst.append([])
        for row in range(len(image)):
            image_lst[channel].append([])
    channel = 0
    while channel in range(len(image[0][0])):
        for row in range(len(image)):
            for column in range(len(image[0])):
                image_lst[channel][row].append(image[row][column][channel])
        channel += 1
    return image_lst


# print(separate_channels([[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
#  [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
#  [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
#  [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]))

def combine_channels(channels):
    image = []
    for row in range(len(channels[0])):
        image.append([])
        for columns in range(len(channels[0][0])):
            image[row].append([])
    column = 0
    while column in range(len(channels[0])):
        for channel in range(len(channels[0][0])):
            for row in range(len(channels)):
                image[column][channel].append(channels[row][column][channel])
        column += 1
    return image


# print(combine_channels([[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
#  [[2, 2, 2], [2, 2, 2], [2, 2, 2], [2, 2, 2]],
#  [[3, 3, 3], [3, 3, 3], [3, 3, 3], [3, 3, 3]]]
# ))

def RGB2grayscale(colored_image):
    one_path_lst = []
    for row in range(len(colored_image)):
        one_path_lst.append([])
        for column in range(len(colored_image[row])):
            one_path_pixel = round((colored_image[row][column][0]) * 0.299 + (colored_image[row][column][1]) * 0.587 + (
            colored_image[row][column][2]) * 0.114)
            one_path_lst[row].append(one_path_pixel)
    return one_path_lst


# print(RGB2grayscale([[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
#  [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
#  [[1, 2, 3], [1, 2, 3], [1, 2, 3]],
#  [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]
# ))

def blur_kernel(size):
    kernel_size = []
    for row in range(size):
        kernel_size.append([])
        for column in range(size):
            kernel_size[row].append(1 / size ** 2)
    return kernel_size


def convlove(image, loc, kernel): #build a mat the size of the jernel with the adjust values according to the location in the image
    i = 0
    mat = [[0] * (kernel) for i in range(kernel)]
    lengh_kernel = (kernel - 1) // 2
    for row in range(loc[0] - lengh_kernel, loc[0] + lengh_kernel + 1):
        j = 0
        for column in range(loc[1] - lengh_kernel, loc[1] + lengh_kernel + 1):
            if column not in range(len(image[0])) or row not in range(len(image)):
                mat[i][j] = image[loc[0]][loc[1]]
            else:
                mat[i][j] = image[row][column]
            j += 1
        i += 1
    return mat


# print(convlove([[0, 1, 2, 0, 1], [1, 2, 2, 0, 0], [0, 1, 2, 1, 0], [0, 2, 1, 1, 0], [0, 0, 1, 0, 2]], (0, 0),
#                blur_kernel(3)
#                ))


def calculate_kernel(mat, kernel):# this function calculates a single pixel with a kernel
    new_loc = 0
    for row in range(kernel):
        for column in range(kernel):
            new_loc += mat[row][column] * blur_kernel(kernel)[row][column]
            if new_loc >= 255:
                new_loc = 255
            if new_loc <= 0:
                new_loc = 0
    return round(new_loc)


# print(calculate_kernel([[0, 0, 0], [0, 0, 1], [0, 1, 2]], blur_kernel(3)))



def apply_kernel(image, kernel):
    new_image = [[0] * len(image[0]) for i in range(len(image))]
    for row in range(len(image)):
        for column in range(len(image[row])):
            new_image[row][column] = calculate_kernel(convlove(image,(row, column), kernel), kernel)
    return new_image

# print(apply_kernel([[10, 20, 30, 40, 50],
# [8, 16, 24, 32, 40],
# [6, 12, 18, 24, 30],
# [4, 8, 12, 16, 20]], blur_kernel(5)))

def bilinear_interpolation(image, y, x):
    if y > len(image)-1:
        y = len(image) - 1
    if x > len(image[0])-1:
        x = len(image[0]) - 1
    a = image[math.floor(y)][math.floor(x)]
    b = image[math.ceil(y)][math.floor(x)]
    c = image[math.floor(y)][math.ceil(x)]
    d = image[math.ceil(y)][math.ceil(x)]
    dx = x - math.floor(x)
    dy = y - math.floor(y)
    new_pixel = round(a * (1 - dx) * (1 - dy) + b * dy * (1 - dx) + c * dx * (1 - dy) + d * dx * dy)
    return new_pixel
# print(bilinear_interpolation([[15,30,45,60,75],[90,105,120,135,150],[165,180,195,210,225]], 0.8,8/3))



def resize(image, new_height, new_width):
    resized_image = [[0] * new_width for i in range(new_height)] #create an empty rezised image
    for row in range(new_height):
        for column in range(new_width):
            y = (row * (len(image))) / (new_height) #get source location
            x = (column * len(image[0])) / (new_width)
            resized_image[row][column] = (bilinear_interpolation(image,y, x)) #calculates the pixel at the destination image
    resized_image[0][0] = image[0][0]
    resized_image[0][-1] = image[0][-1]
    resized_image[-1][0] = image[-1][0]
    resized_image[-1][-1] = image[-1][-1]
    return resized_image
# print(resize([[1,2,3],[1,2,3],[1,2,3]],4,4))

def rotate_90(image, str):
    rotated_img = []
    for row in range(len(image[0])):
        rotated_img.append([])
        for column in range(len(image)):
            rotated_img[row].append(0)
    if str == "R":
        for row in range(len(rotated_img)):
            for column in range(len(image[0])):
                if row not in range(len(image)) or column not in range(len(image[0])):
                    break
                else:
                    rotated_img[column][row] = image[len(image)- 1 - row][column]
    if str == "L":
        for row in range(len(rotated_img)):
            for column in range(len(image[0])):
                if row not in range(len(image)) or column not in range(len(image[0])):
                    break
                else:
                    rotated_img[column][row] = image[row][len(image[0]) - 1 -column]
    return rotated_img

# print(rotate_90([[[1,2,3],[4,5,6],],[[0,5,9],[255,200,7]]],"L"))
def get_threshold(blur_matrix, c):
    threshold = 0
    for i in range(len(blur_matrix)):
        for j in range(len(blur_matrix[0])):
            threshold += blur_matrix[i][j]
    threshold = threshold / (len(blur_matrix) * len(blur_matrix[0])) - c
    return threshold

# def blur_image(image, blur_size):
#     blured_image = image
#     kernel = blur_kernel(blur_size)
#     for row in range(len(blured_image)):
#         for column in range(len(blured_image[0])):
#


def get_edges(image, blur_size, block_size,c):
    edged_image = apply_kernel(image, blur_size)
    for row in range(len(edged_image)):
        for column in range(len(edged_image[0])):
            blur_matrix = convlove(edged_image,(row,column), block_size)
            if edged_image[row][column] < int(get_threshold(blur_matrix, c)):
                edged_image[row][column] = 0
            else:
                edged_image[row][column] = 255
    return edged_image

# print(get_edges([[200, 50, 200], [200, 50, 200], [200, 50, 200]], 1, 3,
#                      10))


def quantize(image, N):
    quantize_image = image
    for row in range(len(image)):
        for column in range(len(image[0])):
            quantize_image[row][column] = round(math.floor(image[row][column] * (N / 256)) * 255 / (N - 1))
    return quantize_image
# print(quantize([[0, 50, 100], [150, 200, 250]], 8))

def quantize_colored_image(image, N):
    quantize_image = image
    for row in range(len(image)):
        for column in range(len(image[0])):
            for channel in range(len(image[row][column])):
                quantize_image[row][column][channel] = round(math.floor(image[row][column][channel] * (N / 256)) * 255 / (N - 1))
    return quantize_image

# print(quantize_colored_image([[[33,5],[34,2]],[[24,43],[45,56]],[[87,76],[65,54]]], 30))
def check_if_colorful(image):
    if type(image[0][0]) is list:
        return True
    else:
        return False
def apply_colorful_kernel(image,kernel):
    seprated_img = separate_channels(image)
    apply_kernel(seprated_img, kernel)
    return combine_channels(apply_kernel(seprated_img, kernel))
def edges_validity():
    edged_input = input("insert block size, blur size and threshold constant")
    if type(edged_input) is not tuple:
        return False
    else:
        if edged_input[0].isnumeric() == False or edged_input[1].isnumeric() == False:
            return False
        if int(edged_input[0]) <=0 or int(edged_input[1]) <= 0 or int(edged_input[0]) % 2 == 0 or int(edged_input[1]) % 2 == 0:
            return False
        if edged_input[2] < 0:
            return False
    return edged_input


#
# if __name__ == '__main__':
#     new_image = ex5_helper.load_image()
#     action_lst = ['1','2','3','4','5','6','7','8']
#     action = input("choose action to make")
#     while action not in action_lst:
#          action = input("please insert a valid action from 1-8")
#     if action == '1':
#          new_image = separate_channels(image)
#     if action == '2':
#         kernel = input("insert kernel size")
#         while kernel <=0 or kernel % 2 == 0 or type(kernel) is not int:
#             kernel = input("insert a vaild kernel size")
#         if check_if_colorful(new_image) is False:
#             new_image = apply_kernel(new_image, kernel)
#         else:
#             new_image = apply_colorful_kernel(new_image, kernel)
#     if action == '3':
#         sizes = input("insert number of rows and columns at the new image")
#         while  type(sizes) is not tuple or len(sizes) != 2 or sizes[0] <=  1 or sizes[1] <= 1:
#             sizes = input("insert number of rows and columns at the new image")
#         new_image = resize(new_image, sizes[0], sizes[1])
#     if action == '4':
#         dirction_lst = ['R','L']
#         round_direction = input("insert the round diraction")
#         while round_direction not in dirction_lst:
#             round_direction = input("insert the round diraction R or L")
#          new_image = rotate_90(new_image, round_direction)
#     if action == '5':
#         while edges_validity() == False:
#             edged_input = edges_validity()
#             if check_if_colorful(new_image) == True:
#                  new_image = get_edges(separate_channels(new_image),int(edged_input[0]),int(edged_input[1]), int(edged_input[2]))
#     if action == '6':
#         num_of_shades = input("insert number of shades")
#         while num_of_shades.isnumeric() == False or int(num_of_shades) <= 1:
#             num_of_shades = input("insert a natural number of shades")
#         if check_if_colorful(new_image) == True:
#             new_image = combine_channels(quantize(separate_channels(new_image)), int(num_of_shades))
#         else:
#             new_image = quantize(new_image, int(num_of_shades))
#     if action == '7':
#         ex5_helper.show_image(new_image)
#     if action == '8':
#         ex5_helper.save_image(input("insert path to save the image"))
#         return


print(check_if_colorful([[1,2,3],[2,3,4]]))

















