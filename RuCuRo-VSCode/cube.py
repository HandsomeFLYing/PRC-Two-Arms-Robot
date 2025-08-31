import os
import time
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as p3d

x_point=150; y_point=75 ;mid_point=35
#魔方面位置
polst = 2
if(polst == 0):
    points_list = [(10+x_point,315-y_point),#r面的1边点
                (260,290-mid_point),#z面的1边点
                (500-x_point,315-y_point),#l面的1边点
                (500-x_point,y_point),#l面的2边点
                (260,10+mid_point),#z面的2边点
                (10+x_point,y_point)#r面的2边点
                ]#上下颠倒
elif(polst==1):
    points_list = [(500-x_point,y_point),#r面的1边点
                (260,20+mid_point),#z面的1边点
                (10+x_point,y_point),#l面的1边点
                (10+x_point,315-y_point),#l面的2边点
                (260,300-mid_point),#z面的2边点
                (500-x_point,315-y_point)#r面的2边点
                ] #左右颠倒
elif(polst==2):
    points_list = [(x_point-30,y_point-12),#左面的1边点
                (240,mid_point-10),#中面的1边点
                (500-x_point,y_point),#右面的1边点
                (500-x_point,345-y_point),#右面的2边点
                (240,305),#中面的2边点
                (120,270)#左面的2边点
                ] #正常画面
elif(polst==3):               
    points_list = [(500-x_point,315-y_point),#r面的1边点
                (260,290-mid_point),#z面的1边点
                (10+x_point,315-y_point),#l面的1边点
                (10+x_point,y_point),#l面的2边点
                (260,10+mid_point),#z面的2边点
                (500-x_point,y_point)#r面的2边点
                ] #全部颠倒
               

# 轮廓处理和图片矫正及分割
def contour_process(in_img,out_img_shape):
    # 左右图分割和文档矫正
    left_last_points = np.float32([points_list[0],points_list[1],points_list[5],points_list[4]])
    right_last_points = np.float32([points_list[1],points_list[2],points_list[4],points_list[3]])
    new_points = np.float32([[0,0],[out_img_shape[0],0],[0,out_img_shape[1]],[out_img_shape[0],out_img_shape[1]]])
    ML = cv.getPerspectiveTransform(left_last_points,new_points)
    left_img = cv.warpPerspective(in_img,ML,(out_img_shape[0],out_img_shape[1]))
    MR = cv.getPerspectiveTransform(right_last_points,new_points)
    right_img = cv.warpPerspective(in_img,MR,(out_img_shape[0],out_img_shape[1]))

    return left_img, right_img


# 魔方颜色序列调整
def get_case_by_sort_str(sort_str):
    # 定义合法的映射关系（字典）#
    # {'white': '白色','red': '红色','green': '绿色','yellow': '黄色','orange': '橙色','blue': '蓝色'}
    sort_mapping = {
        ('gw', 'yr', 'ob'): 0,
        ('gr', 'oy', 'wb'): 1,#正常
        ('go', 'rw', 'yb'): 2,
        ('gy', 'wo', 'rb'): 3,
        ('wg', 'ry', 'bo'): 4,
        ('rg', 'yo', 'bw'): 5,
        ('og', 'wr', 'by'): 6,
        ('yg', 'ow', 'br'): 7
    }
    for keys, case_val in sort_mapping.items():
        if sort_str in keys:
            return case_val
    return -1  # 无效标识
def cube_list_sort():
    f = open('data/sort.txt',mode='r',encoding='utf-8')
    sort_str = f.read(2)
    #case = -1
    # print(sort_list)
    case = get_case_by_sort_str(sort_str)
    print("（摆放状态 \t"+ str(sort_str) + " | " +str(case))
    # 不变，顺时针，逆时针，倒转
    sort_way = [[0,1,2,3,4,5,6,7,8],
                [6,3,0,7,4,1,8,5,2],
                [2,5,8,1,4,7,0,3,6],
                [8,7,6,5,4,3,2,1,0]]
    
    sort_case = [[2,2,2,0,3,3],
                 [2,0,0,0,1,1],
                 [3,2,3,1,3,2],
                 [3,0,1,1,1,0],
                 [1,1,1,3,0,0],
                 [1,3,3,3,2,2],
                 [0,1,0,2,0,1],
                 [0,3,2,2,2,3]]

    #列表
    color = ['white','red','green','yellow','orange','blue']
    color_ = ['w','r','g','y','o','b']

    for i in range(len(color)):
        f = open('data/'+color[i]+'.txt',mode='r',encoding='utf-8')
        color_list = []
        rule_list = []
        for line in f.readlines(): #依次读取每行
            lines = line.strip()
            rule_list.append(lines) #去掉每行头尾空白
        # print(rule_list)
        for j in sort_way[sort_case[case][i]]:
            color_list.append(str(rule_list[j]))
        # print(color_list)
        f.close()
        f = open('data/'+color_[i]+'.txt',mode='w',encoding='utf-8')
        #print("列：" + color_[i])
        for i in range(len(color_list)):
            f.write(color_list[i])
            f.write('\n')
        f.close()

        
# 图片矫正并保存为每个点的值
def img2points(img,atxt = "o"):
    left_img,right_img = contour_process(img,[30,30])
    cv.imwrite('./picture/'+str(time.process_time())+'left_img_'+atxt+'.png',left_img)
    cv.imwrite('./picture/'+str(time.process_time())+'right_img_'+atxt+'.png',right_img)

    hsv_left_img = cv.cvtColor(left_img,cv.COLOR_RGB2HSV)
    hsv_right_img = cv.cvtColor(right_img,cv.COLOR_RGB2HSV)

    lab_left_img = cv.cvtColor(left_img,cv.COLOR_RGB2LAB)
    lab_right_img = cv.cvtColor(right_img,cv.COLOR_RGB2LAB)


    f = open('./data/hsv_points.txt',mode='a',encoding='utf-8')
    for i in range(int(hsv_left_img.shape[0]/6),int(hsv_left_img.shape[0]),int(hsv_left_img.shape[0]/3)):
        for j in range(int(hsv_left_img.shape[1]/6),int(hsv_left_img.shape[1]),int(hsv_left_img.shape[1]/3)):
            f.write(str(hsv_left_img[i,j][0])+'\n')
            f.write(str(hsv_left_img[i,j][1])+'\n')
            f.write(str(hsv_left_img[i,j][2])+'\n\n')
    for i in range(int(hsv_right_img.shape[0]/6),int(hsv_right_img.shape[0]),int(hsv_right_img.shape[0]/3)):
        for j in range(int(hsv_right_img.shape[1]/6),int(hsv_right_img.shape[1]),int(hsv_right_img.shape[1]/3)):
            f.write(str(hsv_right_img[i,j][0])+'\n')
            f.write(str(hsv_right_img[i,j][1])+'\n')
            f.write(str(hsv_right_img[i,j][2])+'\n\n')
    f.close()

    f = open('./data/lab_points.txt',mode='a',encoding='utf-8')
    for i in range(int(lab_left_img.shape[0]/6),int(lab_left_img.shape[0]),int(lab_left_img.shape[0]/3)):
        for j in range(int(lab_left_img.shape[1]/6),int(lab_left_img.shape[1]),int(lab_left_img.shape[1]/3)):
            f.write(str(lab_left_img[i,j][0])+'\n')
            f.write(str(lab_left_img[i,j][1])+'\n')
            f.write(str(lab_left_img[i,j][2])+'\n\n')
    for i in range(int(lab_right_img.shape[0]/6),int(lab_right_img.shape[0]),int(lab_right_img.shape[0]/3)):
        for j in range(int(lab_right_img.shape[1]/6),int(lab_right_img.shape[1]),int(lab_right_img.shape[1]/3)):
            f.write(str(lab_right_img[i,j][0])+'\n')
            f.write(str(lab_right_img[i,j][1])+'\n')
            f.write(str(lab_right_img[i,j][2])+'\n\n')
    f.close()

# 聚类颜色识别 K-Means聚类颜色识别
def kmeans(gamut_type):
    kmeans_points_list = []
    f = open('./data/'+gamut_type+'_points.txt',mode='r',encoding='utf-8')
    for line in f.readlines(): #依次读取每行
        line_list = line.strip()
        if not(line_list == ''):
            kmeans_points_list.append(int(line_list)) #去掉每行头尾空白
    points_array=np.array(kmeans_points_list)
    points_array=points_array.reshape(-1,3)
    points = np.float32(points_array)
    # print(points)

    # 定义停止标准，应用K均值
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1)
    ret,label,center=cv.kmeans(points,6,None,criteria,10,cv.KMEANS_RANDOM_CENTERS)
#     print(type(label))
#     print(type(center))
    color_dict = {}
    if(gamut_type=='lab'):
        wo_temp = []
        for i in range(6):
            if (i == np.argsort(center,axis=0)[0][0]):
                color_dict['red'] = i
            elif(i == np.argsort(center,axis=0)[1][0]):
                color_dict['blue'] = i
            elif(i == np.argsort(center,axis=0)[0][1]):
                color_dict['green'] = i
            elif(i == np.argsort(center,axis=0)[1][1]):
                color_dict['yellow'] = i
            else:
                wo_temp.append(i)

        for i in range(6):
            if(wo_temp[0] == np.argsort(center,axis=0)[i][2]):
                color_dict['white'] = wo_temp[1]
                color_dict['orange'] = wo_temp[0]
                break
            elif(wo_temp[1] == np.argsort(center,axis=0)[i][2]):
                color_dict['orange'] = wo_temp[1]
                color_dict['white'] = wo_temp[0]
                break
    #print(color_dict)
    elif(gamut_type=='hsv'):
        gy_temp = []
        for i in range(6):
            if (i == np.argsort(center,axis=0)[0][0]):
                color_dict['blue'] = i
            elif(i == np.argsort(center,axis=0)[1][0]):
                color_dict['white'] = i
            elif(i == np.argsort(center,axis=0)[2][0]):
                color_dict['green'] = i
            elif(i == np.argsort(center,axis=0)[3][0]):
                color_dict['yellow'] = i
            elif(i == np.argsort(center,axis=0)[4][0]):
                color_dict['orange'] = i
            elif(i == np.argsort(center,axis=0)[5][0]):
                color_dict['red'] = i
        # for i in range(6):
        #     if (i == np.argsort(center,axis=0)[0][1]):
        #         color_dict['white'] = i
        #     elif(i == np.argsort(center,axis=0)[0][0]):
        #         color_dict['blue'] = i
        #     elif(i == np.argsort(center,axis=0)[5][2]):
        #         color_dict['orange'] = i
        #     elif(i == np.argsort(center,axis=0)[5][0]):
        #         color_dict['red'] = i
        #     else:
        #         gy_temp.append(i)
        # for i in range(6):
        #     if(gy_temp[0] == np.argsort(center,axis=0)[i][0]):
        #         color_dict['green'] = gy_temp[0]
        #         color_dict['yellow'] = gy_temp[1]
        #         break
        #     elif(gy_temp[1] == np.argsort(center,axis=0)[i][0]):
        #         color_dict['green'] = gy_temp[1]
        #         color_dict['yellow'] = gy_temp[0]
        #         break
    #print(color_dict)

    if(len(color_dict) == 6):
        for p in range(6):
            if(label[p*9+4] == color_dict['blue']):
                title_str = "blue"
            elif(label[p*9+4] == color_dict['red']):
                title_str = "red"
            elif(label[p*9+4] == color_dict['orange']):
                title_str = "orange"
            elif(label[p*9+4] == color_dict['white']):
                title_str = "white"
            elif(label[p*9+4] == color_dict['green']):
                title_str = "green"
            elif(label[p*9+4] == color_dict['yellow']):
                title_str = "yellow"
            f = open('./data/sort.txt',mode='a',encoding='utf-8')
            f.write(title_str[0])
            f.close()
            f = open('./data/'+title_str+'.txt',mode='a',encoding='utf-8')
            for i in range(9):
                if(label[p*9+i] == color_dict['blue']):
                    color_str = "blue\n"
                elif(label[p*9+i] == color_dict['red']):
                    color_str = "red\n"
                elif(label[p*9+i] == color_dict['orange']):
                    color_str = "orange\n"
                elif(label[p*9+i] == color_dict['white']):
                    color_str = "white\n"
                elif(label[p*9+i] == color_dict['green']):
                    color_str = "green\n"
                elif(label[p*9+i] == color_dict['yellow']):
                    color_str = "yellow\n"
                f.write(color_str)
            f.close()
    return points, label, center, color_dict
    # print(center)
    # print(color_dict)
    # print(np.argsort(center,axis=0))

# 绘制数据
from typing import Dict, List, Tuple, Optional
def plot(points: np.ndarray, 
         labels: np.ndarray, 
         centers: np.ndarray, 
         color_map: Dict[str, int],
         title: str = "魔方聚类识别可视化",
         point_size: int = 20,
         center_size: int = 40,
         center_marker: str = 's',
         axis_labels: Tuple[str, str, str] = ('X', 'Y', 'Z'),
         show_axes: bool = True,
         show_grid: bool = True,
         figsize: Tuple[int, int] = (10, 8),
         colors: Optional[List[str]] = None) -> None:
    """
    3D点云聚类结果可视化
    
    参数:
        points: 点云数据，形状为 (n_points, 3)
        labels: 点云标签，形状为 (n_points,)
        centers: 聚类中心，形状为 (n_centers, 3)
        color_map: 标签到颜色名称的映射字典
        title: 图表标题
        point_size: 点的大小
        center_size: 聚类中心的大小
        center_marker: 聚类中心的标记样式
        axis_labels: 坐标轴标签
        show_axes: 是否显示坐标轴
        show_grid: 是否显示网格
        figsize: 图表大小
        colors: 自定义颜色列表，如果为None则使用默认颜色
    """
    # 设置中文字体
    plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    # 创建图形和3D坐标轴
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    # 默认颜色列表
    default_colors = ['b', 'r', 'm', 'c', 'g', 'y', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray']
    colors = colors or default_colors
    # 按标签分组并绘制点云
    for i, (color_name, label_value) in enumerate(color_map.items()):
        # 获取对应标签的点
        cluster_points = points[labels.ravel() == label_value]
        # 确保有数据点
        if len(cluster_points) > 0:
            # 选择颜色，循环使用颜色列表
            color = colors[i % len(colors)]
            # 绘制点云
            ax.scatter(
                cluster_points[:, 0], 
                cluster_points[:, 1], 
                cluster_points[:, 2],
                c=color, 
                s=point_size, 
                label=f'{color_name} ({len(cluster_points)}点)'
            )
    # 绘制聚类中心
    if centers.size > 0:
        ax.scatter(
            centers[:, 0], 
            centers[:, 1], 
            centers[:, 2],
            s=center_size, 
            c='k', 
            marker=center_marker, 
            label='聚类中心'
        )
    # 设置图表属性
    ax.set_title(title)
    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])
    ax.set_zlabel(axis_labels[2])
    # 显示网格和坐标轴
    ax.grid(show_grid)
    if not show_axes:
        ax.axis('off')
    # 添加图例
    ax.legend()
    # 调整视角
    ax.view_init(elev=30, azim=45)
    # 显示图表
    plt.tight_layout()
    plt.show()

#kmeans()

#读取数据与判断完整性
def check_data():
    color = ['white','red','green','yellow','orange','blue']
    if (os.path.exists('./data/blue.txt') and os.path.exists('./data/green.txt') and
        os.path.exists('./data/red.txt') and os.path.exists('./data/orange.txt') and
        os.path.exists('./data/white.txt') and os.path.exists('./data/yellow.txt')):
        for j in range(6):
            if(j == 5):
                return 1
            num = 0
            for i in range(len(color)):
                with open('data/'+color[i]+'.txt',mode='r',encoding='utf-8') as f:
                    for line in f.readlines(): #依次读取每行
                        lines = line.strip()
                        if(lines == color[j]):
                            num += 1
                        # print(num)
            if(num == 9):
                continue
            else:#测试false
                for i in range(6):
                    if os.path.exists('data/'+color[i]+'.txt'):
                        os.remove('data/'+color[i]+'.txt')
                    if os.path.exists('data/sort.txt'):
                        os.remove('data/sort.txt')
                print("（remove）01")
                break
    else:#测试false
        for i in range(6):
            if os.path.exists('data/sort.txt'):
                os.remove('data/sort.txt')
            if os.path.exists('data/'+color[i]+'.txt'):
                os.remove('data/'+color[i]+'.txt')
        print("（remove）02")
        return 0

# print(check_data())

#图片灰度检查
from typing import Tuple
def check_light(image_path: str) -> Tuple[float, str]:
    """
    检查图像亮度，判断图像是过亮、过暗还是亮度正常
    
    参数:
        image_path: 图像文件路径
    
    返回:
        Tuple: 包含亮度系数和亮度状态描述的元组
    """
    try:
        # 读取图像并转换为灰度图
        img = cv.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"无法读取图像: {image_path}")
            
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
        # 图像基本信息
        height, width = gray_img.shape[:2]
        size = gray_img.size
        
        # 计算灰度均值偏移量
        mean_gray = np.mean(gray_img)
        deviation_from_128 = mean_gray - 128
        
        # 使用向量化操作替代循环计算平均绝对偏差
        hist = cv.calcHist([gray_img], [0], None, [256], [0, 256])
        x = np.arange(256).reshape(-1, 1)
        mean_abs_deviation = np.sum(np.abs(x - 128 - deviation_from_128) * hist) / size
        
        # 计算亮度系数
        brightness_coefficient = abs(deviation_from_128) / mean_abs_deviation
        
        # 判断亮度状态
        if brightness_coefficient > 1:
            status = "过亮" if deviation_from_128 > 0 else "过暗"
        else:
            status = "亮度正常"
        print(status)  
        return brightness_coefficient 
        
    except Exception as e:
        print(f"处理图像时出错: {e}")
        return -1