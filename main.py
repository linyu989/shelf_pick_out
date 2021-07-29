"""
 @Author       :linyu
 @File         :main.py
 @Description  :主函数
 @Software     :PyCharm
"""
import matplotlib.pyplot as plt
import time

from simulation.storage_map import originMapGroup
from sim_ani.animation_passway import simAnimation
from sim_control import shelf_group_passway

plt.rcParams['figure.dpi'] = 300

'''
主函数
'''


def show_main(real_cells_shape, shelf_carry_num, shelf_unit_num, gif_save=0):
    cell_size = [175, 100]
    # 实际中两列货架为一组中间为过道
    # 图片中是三列货架一组将中间一列货架不填充颜色代表过道
    img_cell_row = int(real_cells_shape[0] * 1.5)
    img_cell_col = real_cells_shape[1]
    cells_shape = [img_cell_row, img_cell_col]
    # 仓库图片大小
    map_h = int((cells_shape[0] + 2) * cell_size[0])
    map_w = int((cells_shape[1] + 2) * cell_size[1])
    map_size = [map_h, map_w]

    '''类实例化'''
    originmap_group = originMapGroup(map_size, cell_size, cells_shape)
    img, alternate_dict_list_group = originmap_group.origin_map()
    ani = simAnimation(alternate_dict_list_group, map_size, cell_size, cells_shape)

    '''随机选取坐标并分组填色'''
    group_update_cells = shelf_group_passway.get_group_update_cells(shelf_carry_num, shelf_unit_num, cells_shape)

    '''动画展示'''
    ani.show_simu_group(group_update_cells, gif_save)


if __name__ == '__main__':
    '''尺寸参数'''

    # 货架行列数
    real_cells_shape = [16, 12]  # 填入货架列数，行数
    # cells_shape = [24, 12]

    # 搬运货架总数shelf_carry_num，每组货架数shelf_unit_num
    shelf_carry_num, shelf_unit_num = 103, 5

    # 是否保存gif图片
    gif_save = 0  # 0表示不保存,1表示保存，默认不保存

    '''运行程序'''
    if shelf_carry_num <= int(real_cells_shape[0] * real_cells_shape[0]):
        start_time = time.time()
        show_main(real_cells_shape, shelf_carry_num, shelf_unit_num, gif_save)
        end_time = time.time()
        print(f'用时:{end_time - start_time}')
    else:
        print("[INFO] Error Shelf carry num !!!")
