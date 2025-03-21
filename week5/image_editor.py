#################################################################
# FILE : image_editor.py
# WRITER : your_name , your_login , your_id
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that...
# STUDENTS I DISCUSSED THE EXERCISE WITH: Bugs Bunny, b_bunny.
#								 	      Daffy Duck, duck_daffy.
# WEB PAGES I USED: www.looneytunes.com/lola_bunny
# NOTES: ...
#################################################################
import copy

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
import math
import sys
import ex5_helper

from typing import Optional


##############################################################################
#                                  Functions                                 #
##############################################################################


def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    image_lst = []
    for channel in range(len(image[0][0])):  # builds an empty image
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


def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    image = []
    for row in range(len(channels[0])):  # builds an empty image
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


def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    one_path_lst = []
    for row in range(len(colored_image)):
        one_path_lst.append([])
        for column in range(len(colored_image[row])):
            one_path_pixel = round((colored_image[row][column][0]) * 0.299 + (colored_image[row][column][1]) * 0.587 + (
                colored_image[row][column][2]) * 0.114)
            one_path_lst[row].append(one_path_pixel)
    return one_path_lst


def blur_kernel(size: int) -> Kernel:
    kernel_size = []
    for row in range(size):
        kernel_size.append([])
        for column in range(size):
            kernel_size[row].append(1 / size ** 2)
    return kernel_size


def calculate_kernel(image,
                     kernel):  # this function calculates a single pixel in the image according to a specific kernel and a mat
    new_loc = 0
    for row in range(len(kernel)):
        for column in range(len(kernel)):
            new_loc += image[row][column] * kernel[row][column]
            if new_loc >= 255:
                new_loc = 255
            if new_loc <= 0:
                new_loc = 0
    return round(new_loc)


def convlove(image, loc,
             kernel):  # build a mat the size of the kernel with the adjust values according to the location in the image
    i = 0
    mat = [[0] * int((kernel)) for i in range(int(kernel))]
    lengh_kernel = (int(kernel) - 1) // 2
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


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    new_image = [[0] * len(image[0]) for i in range(len(image))]
    for row in range(len(image)):
        for column in range(len(image[row])):
            new_image[row][column] = calculate_kernel(convlove(image, (row, column), len(kernel)), kernel)
    return new_image


def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    if x >= len(image[0]) - 1:
        x = math.floor(x)
    if y >= len(image) - 1:
        y = math.floor(y)
    a = image[math.floor(y)][math.floor(x)]
    b = image[math.ceil(y)][math.floor(x)]
    c = image[math.floor(y)][math.ceil(x)]
    d = image[math.ceil(y)][math.ceil(x)]
    dx = x - math.floor(x)
    dy = y - math.floor(y)
    new_pixel = round(a * (1 - dx) * (1 - dy) + b * dy * (1 - dx) + c * dx * (1 - dy) + d * dx * dy)
    return new_pixel


def resize(image, new_height, new_width):
    resized_image = [[0] * new_width for i in range(new_height)]  # create an empty rezised image
    for row in range(new_height):
        for column in range(new_width):
            y = (row * (len(image))) / (new_height)  # get source location
            x = (column * len(image[0])) / (new_width)
            resized_image[row][column] = (
                bilinear_interpolation(image, y, x))  # calculates the pixel at the destination image
    resized_image[0][0] = image[0][0]
    resized_image[0][-1] = image[0][-1]
    resized_image[-1][0] = image[-1][0]
    resized_image[-1][-1] = image[-1][-1]
    return resized_image


def rezise_colorful(image, new_height, new_width):
    resized_img = []
    separate_img = separate_channels(new_image)
    for i in range(len(separate_img)):
        resized_img.append(resize(separate_img[i], int(sizes[0]), int(sizes[1])))
    combine_img = []
    for j in range(len(resized_img[0])):
        combine_img.append(combine_channels(resized_img))
    return combine_img


def rotate_90(image: Image, direction: str) -> Image:
    rotated_img = []
    for row in range(len(image[0])):
        rotated_img.append([])
        for column in range(len(image)):
            rotated_img[row].append(0)
    if direction == "R":
        for row in range(len(rotated_img)):
            for column in range(len(image[0])):
                if row not in range(len(image)) or column not in range(len(image[0])):
                    break
                else:
                    rotated_img[column][row] = image[len(image) - 1 - row][column]
    if direction == "L":
        for row in range(len(rotated_img)):
            for column in range(len(image[0])):
                if row not in range(len(image)) or column not in range(len(image[0])):
                    break
                else:
                    rotated_img[column][row] = image[row][len(image[0]) - 1 - column]
    return rotated_img


def get_threshold(blur_matrix, c):
    threshold = 0
    for i in range(len(blur_matrix)):
        for j in range(len(blur_matrix[0])):
            threshold += blur_matrix[i][j]
    threshold = threshold / (len(blur_matrix) * len(blur_matrix[0])) - c
    return threshold


def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    edged_image = apply_kernel(image, blur_kernel(blur_size))
    for row in range(len(edged_image)):
        for column in range(len(edged_image[0])):
            blur_matrix = convlove(edged_image, (row, column), block_size)
            if edged_image[row][column] < int(get_threshold(blur_matrix, c)):
                edged_image[row][column] = 0
            else:
                edged_image[row][column] = 255
    return edged_image


def get_edges_colorful(image, blur_size, block_size, c):
    edged_img = []
    separate_img = separate_channels(image)
    for i in range(len(separate_img)):
        edged_img.append(get_edges(separate_img[i], blur_size, block_size, c))
    combine_img = (combine_channels(edged_img))
    new_image = combine_img
    return new_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    quantize_image = copy.deepcopy(image)
    for row in range(len(image)):
        for column in range(len(image[0])):
            quantize_image[row][column] = round(math.floor(image[row][column] * (N / 256)) * 255 / (N - 1))
    return quantize_image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    quantize_image = copy.deepcopy(image)
    for row in range(len(image)):
        for column in range(len(image[0])):
            for channel in range(len(image[row][column])):
                quantize_image[row][column][channel] = round(
                    math.floor(image[row][column][channel] * (N / 256)) * 255 / (N - 1))
    return quantize_image


def check_if_colorful(image):
    if type(image[0][0]) is list:
        return True
    else:
        return False


def apply_colorful_kernel(image, kernel):
    seprated_img = separate_channels(image)
    for j in range(len(seprated_img)):
        apply_kernel(seprated_img[j], kernel)
    return combine_channels(seprated_img)


def edges_validity():
    edged_input = (input("insert block size"), input("insert  blur size"), input("insert threshold constant"))
    if type(edged_input) is not tuple:
        return False
    else:
        if edged_input[0].isnumeric() == False or edged_input[1].isnumeric() == False:
            return False
        if int(edged_input[0]) <= 0 or int(edged_input[1]) <= 0 or int(edged_input[0]) % 2 == 0 or int(
                edged_input[1]) % 2 == 0:
            return False
        if int(edged_input[2]) < 0:
            return False
    return edged_input


if __name__ == '__main__':
    edit_image = True
    new_image = copy.deepcopy(ex5_helper.load_image(sys.argv[1]))
    action_lst = [1, 2, 3, 4, 5, 6, 7, 8]
    while edit_image:
        action = int(input("choose action to make"))
        while action == '\n' or action not in action_lst:
            action = int(input("please insert a valid action from 1-8"))
        if action == 1:
            if check_if_colorful(new_image):
                new_image = RGB2grayscale(new_image)
            else:
                print("the image is already grey")
            ex5_helper.show_image(new_image)
        if action == 2:
            kernel = (input("insert kernel size"))
            while int(kernel) <= 0 or int(kernel) % 2 == 0 or kernel.isnumeric() == False:
                kernel = (input("insert a vaild kernel size"))
            if check_if_colorful(new_image) is False:
                new_image = apply_kernel(new_image, blur_kernel(int(kernel)))
            else:
                new_image = apply_colorful_kernel(new_image, blur_kernel(int(kernel)))
        if action == 3:
            sizes = (input("insert number of rows"), input("insert number of columns"))
            while type(sizes) is not tuple or len(sizes) != 2 or int(sizes[0]) <= 1 or int(
                    sizes[1]) <= 1 or "\n" in sizes:
                sizes = (input("insert number of rows"), input("insert number of columns"))
            if check_if_colorful(new_image):
                new_image = rezise_colorful(new_image, int(sizes[0]), int(sizes[1]))
            else:
                new_image = resize(new_image, int(sizes[0]), int(sizes[1]))
        if action == 4:
            direction_lst = ['R', 'L']
            round_direction = input("insert the round diraction")
            while round_direction not in direction_lst:
                round_direction = input("insert the round diraction R or L")
            new_image = rotate_90(new_image, round_direction)
        if action == 5:
            edged_input = edges_validity()
            while edged_input == False:
                edged_input = edges_validity()
            if check_if_colorful(new_image) == True:
                new_image = get_edges_colorful(new_image, int(edged_input[0]), int(edged_input[1]), int(edged_input[2]))
            else:
                get_edges(new_image, int(edged_input[0]), int(edged_input[1]), int(edged_input[2]))
        if action == 6:
            num_of_shades = input("insert number of shades")
            while num_of_shades.isnumeric() == False or int(num_of_shades) <= 1:
                num_of_shades = input("insert a natural number of shades")
            if check_if_colorful(new_image) == True:
                new_image = quantize_colored_image(new_image, int(num_of_shades))
            else:
                new_image = quantize(new_image, int(num_of_shades))
        if action == 7:
            ex5_helper.show_image(new_image)
        if action == 8:
            ex5_helper.save_image(input("insert path to save the image"))
            edit_image = False
