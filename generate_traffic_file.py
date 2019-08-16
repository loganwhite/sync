#!/usr/bin/python

import ast
import random

import numpy as np
from Settings import *


def generate_traffic_matrix(shape, link_capacity, ratio):
    """
        generate random traffic matrix
        matrix_shape:

        return: traffic matrix
    """
    # traffic_matrix = np.zeros(shape, np.float)
    tmp_random_nums = np.random.f(10, 1, shape[0] * shape[1])
    mean_matrix = sum(tmp_random_nums) / len(tmp_random_nums)
    tmp_random_nums = np.multiply(tmp_random_nums, ratio)
    tmp_random_nums = np.divide(tmp_random_nums, mean_matrix)
    for i in range(len(tmp_random_nums)):
        if tmp_random_nums[i] > 1:
            tmp_random_nums[i] = 1
    np.random.shuffle(tmp_random_nums)
    tmp_random_nums = np.multiply(tmp_random_nums, link_capacity)
    traffic_matrix = np.reshape(tmp_random_nums, shape)

    return traffic_matrix

def save_matrix_list_file(filename, matrix_list):
    """
    save the matrix list to file
    :param filename:
    :param matrix_list:
    :return: no return
    """
    f = open(filename, 'w')
    f.write('%s' % matrix_list)
    f.close()

def read_matrix_list_file(filename):
    """
    read matrix_list from file
    :param filename:
    :return: the matrix list
    """
    f = open(filename, 'r')
    for line in f:
        traffic_matrix_list = ast.literal_eval(line)
        return traffic_matrix_list



def main():
    traffic_gen_ratio = [0.001, 0.002, 0.003, 0.004]
    matrix_num = 10
    filename = 'traffic_matrix_list_r{}'
    for ratio in traffic_gen_ratio:
        matrix_list = []
        for i in range(matrix_num):
            matrix = generate_traffic_matrix((25, 25), link_capacity, ratio)
            matrix_list.append(matrix.tolist())
        filename = filename.format(ratio)
        save_matrix_list_file(filename, matrix_list)


if __name__ == '__main__':
    main()

