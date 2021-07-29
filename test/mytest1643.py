"""
 @Author       :linyu
 @File         :mytest1643.py
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
输入：
1.根据之前生成货架，每个货架都有相应的位置信息
2.假设现在有若干个货架的搬运任务，需要将这些任务进行分组，默认是5个货架一组，如果不足可以少于5个
3.假设货架一列为相邻的货架，每列之间存在过道
4.货架的分组的原则就是，将相同列的放在一起，不同列的则将距离比较近的放在一组
输出
1.用不同的颜色区分各个分组的信息，通过眼睛可以观察到分组是否合理或者更优
'''


def show_main(real_cells_shape, shelf_carry_num, shelf_unit_num, gif_save=0):
    cell_size = [150, 150]
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

    '''随机选取分组填色'''
    group_update_cells = shelf_group_passway.get_group_update_cells(shelf_carry_num, shelf_unit_num, cells_shape)

    '''动画展示'''
    ani.show_simu_group(group_update_cells, gif_save=0)


if __name__ == '__main__':
    '''尺寸参数'''
    real_cells_shape = [16, 12]
    # cells_shape = [24, 12]
    shelf_carry_num, shelf_unit_num = 101, 5
    gif_save = 1

    '''运行程序'''
    start_time = time.time()
    show_main(real_cells_shape, shelf_carry_num, shelf_unit_num, gif_save)
    end_time = time.time()
    print(f'用时:{end_time - start_time}')
