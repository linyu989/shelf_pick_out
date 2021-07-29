# 货架分组仿真

## 功能说明

    生成一定行列的货架摆放并根据任务需求量以最小搬运距离原则将需要搬运的货架分组

## 运行方式

    1.安装requirements.txt里面所有包
    2.运行main.py文件(可根据参数说明修改对应参数)

## 项目结构

    shelf_pick_out
    │  main.py      //主函数
    │          
    ├─data          //资源文件
    │      
    ├─output        //gif输出文件夹
    │      
    ├─simulation
    │  │  storage_map.py    //地图生成与更新
    │          
    ├─sim_ani
    │      animation_passway.py     //动画渲染
    │      
    ├─sim_control
    │      shelf_group_passway.py    //货架分组
    │      
    └─test      //存放测试程序

## 参数说明

    
    #货架行列数
    real_cells_shape = [16, 12] #填入货架列数，行数
    
    #搬运货架总数shelf_carry_num，每组货架数shelf_unit_num
    shelf_carry_num, shelf_unit_num = 103, 5
    
    # 是否保存gif图片
    gif_save = 0  # 0表示不保存,1表示保存，默认不保存