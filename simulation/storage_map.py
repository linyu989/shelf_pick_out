"""
 @Author       :linyu
 @File         :storage_map.py
 @Description  :仓库地图生成与更新
 @Software     :PyCharm
"""
import numpy as np
import matplotlib.pyplot as plt
import random

plt.rcParams['figure.dpi'] = 300  # 分辨率

'''
根据仓库和货架单元尺寸生成仓库地图
地图分组后填充有过道的原始地图
三行一组中间不渲染表示为过道
'''


class originMapGroup():
    def __init__(self, map_size, cell_size, cells_shape):
        self.map_size = map_size
        self.cell_size = cell_size
        self.cells_shape = cells_shape

    # 货架单元渲染
    #
    def render(self, img, corner, size, color):
        # cell坐标点
        start_h, start_w = corner[0], corner[1]
        # size宽高
        size_h, size_w = size[0], size[1]
        # size长宽调节边界避免格子相连
        dh = int(size[0] / 10)
        dw = int(size[1] / 10)

        img[(start_h + dh):(start_h + size_h), (start_w + dw):(start_w + size_w)] = color

        return img

    # 原始地图
    def origin_map(self):
        red = np.zeros(self.map_size, dtype=np.uint8)
        green = np.zeros(self.map_size, dtype=np.uint8)
        blue = np.zeros(self.map_size, dtype=np.uint8)
        red[:, :] = 255
        green[:, :] = 255
        blue[:, :] = 255
        img = np.dstack((red, green, blue))

        shelf_unload_color = [204, 255, 204]
        shelf_load_color = [255, 102, 0]

        cell_size = self.cell_size
        edge_h, edge_w = cell_size[0], cell_size[1]
        cell_coord_h, cell_coord_w = edge_h, edge_w
        corner = None
        dict_list = {}
        flag = 0

        passway_list = []
        count = 1
        for i in range(self.cells_shape[0]):
            passway_list.append(count)
            count += 3
            if count > self.cells_shape[0]: break

        for i in range(self.cells_shape[0]):
            # 对2，5，8，11之类行不填色作过道处理
            if i in passway_list:
                cell_coord_h += cell_size[0]
                continue

            for j in range(self.cells_shape[1]):
                index = [i, j]
                corner = [cell_coord_h, cell_coord_w]
                # 生成{index:[[corner,cell_size,flag=0],}的字典
                dict_list[str(index)] = [corner, cell_size, flag]
                self.render(img, corner, cell_size, shelf_unload_color)
                cell_coord_w += cell_size[1]
            cell_coord_w = edge_w
            cell_coord_h += cell_size[0]

        # print(dict_list)
        return img, dict_list


'''
继承alternateMap的alternateMapGroup类
用来对地图选取一定数量货架分组后填充
'''
'''
可以不用继承
'''


class alternateMapGroup():
    '''
    随机选择元素并分组更新地图
    '''

    def __init__(self, map_size, alternate_cells_dict, cells_shape):
        self.map_size = map_size
        self.alternate_cells_dict = alternate_cells_dict
        self.cells_shape = cells_shape

    def alternate_cells_render_group(self, img, corner, cell_size, flag):
        color = [204, 255, 204] if flag == 0 else [255, 102, 0]

        if flag == 'deep_red':
            # color = [254, 67, 101]
            color = [255, 0, 255]
        elif flag == 'low_red':
            # color = [252, 157, 154]
            color = [0, 255, 0]
        elif flag == 'low_yellow':
            # color = [249, 205, 173]
            color = [0, 0, 255]
        elif flag == 'low_cyan':
            # color = [200, 200, 169]
            color = [255, 255, 0]

        start_h, start_w = corner[0], corner[1]
        size_h, size_w = cell_size[0], cell_size[1]
        dh = int(cell_size[0] / 5)
        dw = int(cell_size[1] / 5)

        img[int(start_h + dh):(start_h + size_h), int(start_w + dw):(start_w + size_w)] = color

        return img

    '''
    渲染图象与真实图像于y=x对称
    '''

    def img_symmtry_rotation(self, img):
        row, col, channel = img.shape
        img_real_r = np.zeros((col, row), dtype=np.uint8)
        img_real_g = np.zeros((col, row), dtype=np.uint8)
        img_real_b = np.zeros((col, row), dtype=np.uint8)
        img_real = np.dstack((img_real_r, img_real_g, img_real_b))

        for i in range(row):
            img_real[:, i] = img[i, :]
            # img_real[::-1, i] = img[i, :]

        return img_real

    def alternate_map_group(self, map_size, alternate_cells_dict, cells_shape):
        red = np.zeros(map_size, dtype=np.uint8)
        green = np.zeros(map_size, dtype=np.uint8)
        blue = np.zeros(map_size, dtype=np.uint8)
        red[:, :] = 255
        green[:, :] = 255
        blue[:, :] = 255
        img = np.dstack((red, green, blue))

        edge_h, edge_w = 0, 0
        passway_list = []
        count = 1
        for i in range(self.cells_shape[0]):
            passway_list.append(count)
            count += 3
            if count > self.cells_shape[0]: break

        for i in range(cells_shape[0]):
            if i in passway_list: continue
            for j in range(cells_shape[1]):
                index = [i, j]
                corner = alternate_cells_dict[str(index)][0]
                corner = [corner[0] + edge_h, corner[1] + edge_w]
                cell_size = alternate_cells_dict[str(index)][1]
                flag = alternate_cells_dict[str(index)][2]
                self.alternate_cells_render_group(img, corner, cell_size, flag)

        # 将图像关于y=x对称
        img=self.img_symmtry_rotation(img)

        return img

    def update_alternate_map_group(self, map_size, update_cells, cells_shape):
        alternate_cells_dict = self.alternate_cells_dict
        new_cells_dict = alternate_cells_dict

        for cell in update_cells:
            [index, flag] = cell
            new_cells_dict[str(index)][-1] = flag

        img = self.alternate_map_group(map_size, new_cells_dict, cells_shape)

        return img


def plt_show(img):
    print("imgreal================================")
    print(img.shape, img.dtype)

    plt.imshow(img)
    # plt.axis('off')

    # 保存图片
    # plt.savefig(f'./output/origin_map_{str(random.randint(0,9999))}.png', dpi=700)

    plt.show()


if __name__ == '__main__':
    map_h, map_w = 3840, 2160
    map_size = [map_h, map_w]
    cell_size = [150, 150]
    cells_shape = [24, 12]

    # 字典直接内部打印不用返回，该函数还需要外部调用只需要img
    # img, dict_list = origin_map(map_size, cell_size, cell_num)
    # img = origin_map(map_size, cell_size, cells_shape)

    # print(dict_list)

    originmap = originMapGroup(map_size, cell_size, cells_shape)

    origin_map_img, alternate_dict_list = originmap.origin_map()

    alter_map = alternateMapGroup(map_size, alternate_dict_list, cells_shape)

    '''
    # 更新地图
    update_cells = []
    flag = 1
    # for num in range(random.randint(min(cells_shape), cells_shape[0] * cells_shape[1])):
    for num in range(100):
        index = [np.random.randint(0, cells_shape[0]), np.random.randint(0, cells_shape[1])]
        update_cells.append([index, flag])

    print(update_cells)

    img = alter_map.update_alternate_map(map_size, update_cells, cells_shape)
    '''

    # 四色更新地图
    shelf_group_list_flat = [[[0, 0], 'deep_red'], [[0, 1], 'deep_red'], [[0, 2], 'deep_red'], [[0, 3], 'deep_red'],
                             [[0, 4], 'deep_red'],
                             [[1, 0], 'low_red'], [[1, 3], 'low_red'], [[1, 4], 'low_red'], [[1, 7], 'low_red'],
                             [[1, 9], 'low_red'],
                             [[1, 10], 'low_yellow'], [[2, 3], 'low_yellow'], [[2, 0], 'low_yellow'],
                             [[3, 2], 'low_yellow'],
                             [[3, 4], 'low_yellow'], [[3, 5], 'low_cyan'], [[3, 7], 'low_cyan'], [[3, 9], 'low_cyan'],
                             [[4, 7], 'low_cyan'],
                             [[4, 3], 'low_cyan'], [[5, 0], 'deep_red'], [[5, 2], 'deep_red'], [[5, 3], 'deep_red'],
                             [[5, 4], 'deep_red'],
                             [[5, 5], 'deep_red'], [[5, 10], 'low_red'], [[6, 8], 'low_red'], [[6, 5], 'low_red'],
                             [[6, 3], 'low_red'],
                             [[7, 10], 'low_red'], [[7, 8], 'low_yellow'], [[8, 5], 'low_yellow'],
                             [[8, 4], 'low_yellow'],
                             [[8, 3], 'low_yellow'], [[8, 2], 'low_yellow'], [[9, 5], 'low_cyan'],
                             [[10, 9], 'low_cyan'], [[11, 2], 'low_cyan'],
                             [[11, 1], 'low_cyan'], [[11, 0], 'low_cyan'], [[12, 3], 'deep_red'], [[13, 2], 'deep_red'],
                             [[13, 1], 'deep_red'],
                             [[14, 8], 'deep_red'], [[14, 4], 'deep_red'], [[14, 2], 'low_red'], [[14, 1], 'low_red'],
                             [[14, 0], 'low_red'],
                             [[15, 8], 'low_red'], [[15, 7], 'low_red'], [[15, 6], 'low_yellow'],
                             [[15, 2], 'low_yellow'],
                             [[15, 0], 'low_yellow'], [[16, 2], 'low_yellow'], [[16, 1], 'low_yellow'],
                             [[17, 0], 'low_cyan'],
                             [[17, 3], 'low_cyan'], [[18, 9], 'low_cyan'], [[18, 8], 'low_cyan'], [[18, 7], 'low_cyan'],
                             [[18, 6], 'deep_red'],
                             [[18, 5], 'deep_red'], [[18, 2], 'deep_red'], [[19, 5], 'deep_red'], [[19, 2], 'deep_red'],
                             [[19, 1], 'low_red'],
                             [[20, 10], 'low_red'], [[20, 6], 'low_red'], [[20, 5], 'low_red'], [[20, 4], 'low_red'],
                             [[21, 1], 'low_yellow'],
                             [[21, 2], 'low_yellow'], [[21, 5], 'low_yellow'], [[22, 4], 'low_yellow'],
                             [[22, 1], 'low_yellow']]

    img = alter_map.update_alternate_map_group(map_size, shelf_group_list_flat, cells_shape)

    plt_show(img)
