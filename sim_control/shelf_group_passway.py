"""
 @Author       :linyu
 @File         :shelf_group_passway.py
 @Description  :仓库货架留过道两边可以取货
 @Software     :PyCharm
"""

import random
import numpy as np
import copy

'''
原始仓库地图，随机取shelf_carry个元素，每组shelf_num个元素向上取整为shelf_group组，按四种颜色依次填充
新增处理：过道两边可以取货
'''

'''随机获取shelf_carry_num个索引'''


def get_shelf_carry_random(shelf_carry_num, shelf_unit_num, cells_shape):
    # 索引0开始对于1，4，7，的行索引不取
    passway_list = []
    count = 1
    for i in range(cells_shape[0]):
        passway_list.append(count)
        count += 3
        if count > cells_shape[0]: break

    shelf_carry_list = []
    for i in range(cells_shape[0]):
        # 索引0开始对于1，4，7，的行索引不取
        if i in passway_list: continue

        for j in range(cells_shape[1]):
            index = [i, j]
            shelf_carry_list.append(index)

    shelf_carry_list = random.sample(shelf_carry_list, shelf_carry_num)

    return shelf_carry_list


'''对随机获取到的坐标xy升序排列'''


def get_shelf_carry_row_list(shelf_carry_list):
    shelf_carry_list = sorted(shelf_carry_list, key=lambda x: [x[0], x[1]])
    print(shelf_carry_list)

    # 取出x,y按照行存储
    shelf_carry_list_x = []
    shelf_carry_list_y = []
    shelf_carry_row_list = []

    # 按照行顺序存储
    unit_row_list = []
    for i in range(len(shelf_carry_list)):
        if i == len(shelf_carry_list) - 1:
            unit_row_list.append(shelf_carry_list[i])
            shelf_carry_row_list.append(unit_row_list)
            break

        if shelf_carry_list[i][0] == shelf_carry_list[i + 1][0]:
            # 这里存在问题会少添加shelf_carry_list[i + 1]
            unit_row_list.append(shelf_carry_list[i])
        else:
            # 在这里加上表示到达行尾
            unit_row_list.append(shelf_carry_list[i])
            shelf_carry_row_list.append(unit_row_list)
            unit_row_list = []

    print(shelf_carry_row_list)

    return shelf_carry_row_list


'''两行合并内部按y大小排序'''


def get_shelf_carry_row_list_passway_ydistance(shelf_carry_row_list):
    print(len(shelf_carry_row_list))
    shelf_carry_row_list_passway = []
    temp = []
    # 有一个问题随机取并非每行都能取到
    # 可能最后一个只能单行合并
    for i in range(len(shelf_carry_row_list) - 1):
        # 两行合并
        if 2 * i + 1 <= len(shelf_carry_row_list) - 1:
            row_fir = shelf_carry_row_list[2 * i]
            row_sec = shelf_carry_row_list[2 * i + 1]

            temp = row_fir + row_sec
            shelf_carry_row_list_passway.append(temp)
            # 偶数行到达最后一行
            if 2 * i + 1 == len(shelf_carry_row_list) - 1: break
        else:
            # 最后一组单行存在
            temp = shelf_carry_row_list[2 * i + 1]
            shelf_carry_row_list_passway.append(temp)
            break
    print(shelf_carry_row_list_passway)

    # 内部按照y排序
    dual_row_sorted = []
    list_temp = []
    for i, dual_row in enumerate(shelf_carry_row_list_passway):
        shelf_carry_row_list_passway[i] = sorted(dual_row, key=lambda x: x[1])

    print(shelf_carry_row_list_passway)

    return shelf_carry_row_list_passway


'''z字降维后展开'''


def get_shelf_group_list_passway_zflat(shelf_carry_row_list_passway):
    shelf_group_list_passway_flat = []
    for i in range(len(shelf_carry_row_list_passway)):
        # 按z字排列降维
        if i % 2 == 1:
            shelf_group_list_passway_flat += shelf_carry_row_list_passway[i][::-1]
        else:
            shelf_group_list_passway_flat += shelf_carry_row_list_passway[i]

    print(shelf_group_list_passway_flat)
    print(len(shelf_group_list_passway_flat))

    return shelf_group_list_passway_flat


'''按shelf_unit_num分组'''


def get_shelf_group_list(shelf_group_list_passway_flat, shelf_unit_num):
    len_flat = len(shelf_group_list_passway_flat)
    print(len_flat)

    shelf_unit_group_list = []
    shelf_group_list = []

    for i in range(len_flat):
        shelf_unit_group_list.append(shelf_group_list_passway_flat[i])
        if (len(shelf_unit_group_list) == shelf_unit_num) or (i == len_flat - 1):
            shelf_group_list.append(shelf_unit_group_list)
            shelf_unit_group_list = []
    print(shelf_group_list)

    return shelf_group_list


'''添加flag'''


def add_flag(shelf_group_list):
    shelf_group_list_flag_unit = []
    shelf_group_list_flag = []
    colors = ['deep_red', 'low_red', 'low_yellow', 'low_cyan']
    for i, row in enumerate(shelf_group_list):
        if i % 4 == 0:
            for index in row: shelf_group_list_flag_unit.append([index, colors[0]])
        elif i % 4 == 1:
            for index in row: shelf_group_list_flag_unit.append([index, colors[1]])
        elif i % 4 == 2:
            for index in row: shelf_group_list_flag_unit.append([index, colors[2]])
        elif i % 4 == 3:
            for index in row: shelf_group_list_flag_unit.append([index, colors[3]])
        shelf_group_list_flag.append(copy.deepcopy(shelf_group_list_flag_unit))

    print(shelf_group_list_flag_unit)
    print(shelf_group_list_flag)

    return shelf_group_list_flag


'''updatecells的列表生成'''


def merge_carry_flag(shelf_carry_list, shelf_group_list_flag):
    group_update_cells = []
    shelf_carry_list = [[i, 1] for i in shelf_carry_list]
    print(shelf_carry_list)

    group_update_cells.append(shelf_carry_list)
    for row in shelf_group_list_flag:
        group_update_cells.append(row)

    print(group_update_cells)
    return group_update_cells


def get_group_update_cells(shelf_carry_num, shelf_unit_num, cells_shape):
    # 随机选取坐标
    shelf_carry_list = get_shelf_carry_random(shelf_carry_num, shelf_unit_num, cells_shape)
    # 排序后按行划分
    shelf_carry_row_list = get_shelf_carry_row_list(shelf_carry_list)
    # 两行合并内部y大小排序
    shelf_carry_row_list_passway = get_shelf_carry_row_list_passway_ydistance(shelf_carry_row_list)
    # 按z顺序并展开成一维
    shelf_group_list_passway_flat = get_shelf_group_list_passway_zflat(shelf_carry_row_list_passway)
    # 按shelf_unit_num分组
    shelf_group_list = get_shelf_group_list(shelf_group_list_passway_flat, shelf_unit_num)
    # 添加flag
    shelf_group_list_flag = add_flag(shelf_group_list)
    # 合并shelf_carry_list与shelf_group_list_flag生成update_cells
    group_update_cells = merge_carry_flag(shelf_carry_list, shelf_group_list_flag)

    return group_update_cells


if __name__ == '__main__':
    shelf_carry_num, shelf_unit_num = 100, 5

    # 随机获取坐标
    # shelf_carry_list = get_shelf_carry(shelf_carry_num, shelf_unit_num)

    shelf_carry_list = [[0, 1], [0, 6], [0, 9], [0, 10], [0, 11], [2, 1], [2, 4], [2, 5], [2, 6], [2, 11], [3, 0],
                        [3, 1], [3, 4], [3, 6], [3, 7], [3, 8], [5, 2], [5, 3], [5, 5], [5, 7], [5, 8], [5, 10],
                        [5, 11], [6, 0], [6, 1], [6, 3], [6, 4], [6, 5], [6, 7], [6, 9], [6, 10], [6, 11], [8, 0],
                        [8, 1], [8, 8], [8, 11], [9, 0], [9, 1], [9, 6], [9, 10], [9, 11], [11, 0], [11, 3], [11, 4],
                        [11, 5], [11, 7], [11, 8], [11, 9], [11, 10], [11, 11], [12, 2], [12, 4], [12, 8], [12, 10],
                        [12, 11], [14, 0], [14, 2], [14, 4], [14, 5], [14, 6], [14, 7], [14, 9], [14, 11], [15, 1],
                        [15, 2], [15, 5], [15, 6], [15, 8], [17, 1], [17, 6], [17, 9], [17, 10], [17, 11], [18, 0],
                        [18, 1], [18, 2], [18, 3], [18, 4], [18, 7], [18, 8], [18, 11], [20, 0], [20, 2], [20, 3],
                        [20, 8], [20, 9], [20, 10], [21, 4], [21, 6], [21, 7], [21, 8], [21, 9], [23, 0], [23, 1],
                        [23, 2], [23, 3], [23, 4], [23, 5], [23, 6], [23, 9]]
    # 排序后按行划分
    shelf_carry_row_list = get_shelf_carry_row_list(shelf_carry_list)
    # 两行合并内部y大小排序
    shelf_carry_row_list_passway = get_shelf_carry_row_list_passway_ydistance(shelf_carry_row_list)
    # 按z顺序并展开成一维
    shelf_group_list_passway_flat = get_shelf_group_list_passway_zflat(shelf_carry_row_list_passway)
    # 按shelf_unit_num分组
    shelf_group_list = get_shelf_group_list(shelf_group_list_passway_flat, shelf_unit_num)
    # 添加flag
    shelf_group_list_flag = add_flag(shelf_group_list)
    # 合并shelf_carry_list与shelf_group_list_flag生成update_cells
    update_cells = merge_carry_flag(shelf_carry_list, shelf_group_list_flag)

    # get_shelf_carry_row_list()

    # get_shelf_carry_row_list_passway()

    # get_shelf_group_list_passway_zflat()

    # get_shelf_group_list()

    # add_flag()

    # shelf_carry_list = [[0, 1], [0, 6], [0, 9], [0, 10], [0, 11], [2, 1], [2, 4], [2, 5], [2, 6], [2, 11], [3, 0],
    #                     [3, 1], [3, 4], [3, 6], [3, 7], [3, 8], [5, 2], [5, 3], [5, 5], [5, 7], [5, 8], [5, 10],
    #                     [5, 11], [6, 0], [6, 1], [6, 3], [6, 4], [6, 5], [6, 7], [6, 9], [6, 10], [6, 11], [8, 0],
    #                     [8, 1], [8, 8], [8, 11], [9, 0], [9, 1], [9, 6], [9, 10], [9, 11], [11, 0], [11, 3], [11, 4],
    #                     [11, 5], [11, 7], [11, 8], [11, 9], [11, 10], [11, 11], [12, 2], [12, 4], [12, 8], [12, 10],
    #                     [12, 11], [14, 0], [14, 2], [14, 4], [14, 5], [14, 6], [14, 7], [14, 9], [14, 11], [15, 1],
    #                     [15, 2], [15, 5], [15, 6], [15, 8], [17, 1], [17, 6], [17, 9], [17, 10], [17, 11], [18, 0],
    #                     [18, 1], [18, 2], [18, 3], [18, 4], [18, 7], [18, 8], [18, 11], [20, 0], [20, 2], [20, 3],
    #                     [20, 8], [20, 9], [20, 10], [21, 4], [21, 6], [21, 7], [21, 8], [21, 9], [23, 0], [23, 1],
    #                     [23, 2], [23, 3], [23, 4], [23, 5], [23, 6], [23, 9]]
    #
    # print(len(shelf_carry_list))
    #
    # list01 = [[0, 0], [2, 0], [0, 1], [2, 2], [0, 2], [2, 3], [0, 6], [2, 6], [0, 9], [2, 9], [0, 10], [3, 2], [5, 2],
    #           [5, 4],
    #           [5, 5], [5, 6], [5, 8], [6, 0], [8, 3], [6, 6], [8, 5], [6, 8], [8, 7], [6, 9], [8, 8], [6, 10], [9, 2],
    #           [11, 0],
    #           [9, 3], [11, 2], [9, 4], [11, 4], [9, 5], [11, 6], [9, 7], [11, 7], [9, 8], [11, 8], [9, 9], [11, 10],
    #           [9, 10],
    #           [12, 2], [14, 1], [12, 3], [14, 4], [12, 4], [14, 5], [12, 7], [14, 9], [12, 8], [14, 10], [15, 0],
    #           [17, 0],
    #           [15, 1], [17, 2], [15, 4], [17, 4], [15, 6], [17, 6], [15, 7], [17, 7], [15, 8], [17, 8], [15, 10],
    #           [18, 0],
    #           [20, 0], [18, 2], [20, 1], [18, 7], [20, 5], [20, 7], [20, 9], [21, 0], [21, 2], [21, 3], [21, 7],
    #           [21, 8]]

    '''
    listzip1 = [[0, 0], [0, 1], [0, 2], [0, 6], [0, 9], [0, 10]]
    listzip2=[[2, 0], [2, 2], [2, 3], [2, 6], [2, 9]]

    len1,len2=len(listzip1),len(listzip2)
    min_len=min(len1,len2)
    max_len_list=listzip1 if len1>len2 else listzip2


    iter_zip = list(zip(listzip1, listzip2))
    print(iter_zip)
    print(iter_zip[0])
    print(type(iter_zip[0]))

    shelf_group_list_passway_alter=[]
    for i in iter_zip:
        shelf_group_list_passway_alter.append(i[0])
        shelf_group_list_passway_alter.append(i[1])
    print(shelf_group_list_passway_alter)
    shelf_group_list_passway_alter+=max_len_list[min_len:]
    print(shelf_group_list_passway_alter)
    '''
