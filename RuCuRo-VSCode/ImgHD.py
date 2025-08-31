import os
import time
import cv2 as cv
import numpy as np
points_list = [
    # 0--1--2
    # |  |  |
    # 5--4--3
    # ##
                (120,63),#左面的1边点
                (240,25),#中面的1边点
                (350,75),#右面的1边点
                (350,270),#右面的2边点
                (240,305),#中面的2边点
                (120,270)#左面的2边点
                ] #正常画面
x_point=80; y_point=20 ;mid_point=35
points_list_cv1 = [
    # 0---1
    # |   |
    # 2---3
    # ##
               #后
               (x_point+20,y_point),#左面的1边点
               (320,mid_point-10),#中面的1边点
               (x_point+15,315-y_point),#左面的2边点
               (310,350-mid_point),#中面的2边点
               #前
               (x_point+50,y_point+40),#中面的1边点
               (325,mid_point+15),#右面的1边点
               (x_point+55,335-y_point),#中面的2边点
               (330,340-mid_point)#右面的2边点
                ] #正常画面
points_list_cv2 = [
    # 1---3  5---7
    # |   |  |   |
    # 0---2  4---6
    # ##
               #后
               (130,285),#0
               (130,75),#1
               (245,330),#2
               (245,35),#3
               #前
               (245,330),#0
               (245,35),#1
               (360,290),#2
               (360,75)#3
                ] #正常画面

# 轮廓处理和图片矫正及分割
def contour_process_fa_img(in0_img,in1_img,out_img_shape):
    # 前后图分割和文档矫正
    left_last_points = np.float32([points_list_cv1[0],points_list_cv1[1],points_list_cv1[2],points_list_cv1[3]])
    right_last_points = np.float32([points_list_cv1[4],points_list_cv1[5],points_list_cv1[6],points_list_cv1[7]])
    new_points = np.float32([[0,0],[out_img_shape[0],0],[0,out_img_shape[1]],[out_img_shape[0],out_img_shape[1]]])
    ML = cv.getPerspectiveTransform(left_last_points,new_points)
    left_img = cv.warpPerspective(in0_img,ML,(out_img_shape[0],out_img_shape[1]))
    MR = cv.getPerspectiveTransform(right_last_points,new_points)
    right_img = cv.warpPerspective(in1_img,MR,(out_img_shape[0],out_img_shape[1]))

    return left_img, right_img

def contour_below_process(in_img,out_img_shape):
    # 下左右图分割和文档矫正
    left_last_points = np.float32([points_list_cv2[0],points_list_cv2[1],points_list_cv2[2],points_list_cv2[3]])
    right_last_points = np.float32([points_list_cv2[4],points_list_cv2[5],points_list_cv2[6],points_list_cv2[7]])
    new_points = np.float32([[0,0],[out_img_shape[0],0],[0,out_img_shape[1]],[out_img_shape[0],out_img_shape[1]]])
    ML = cv.getPerspectiveTransform(left_last_points,new_points)
    left_img = cv.warpPerspective(in_img,ML,(out_img_shape[0],out_img_shape[1]))
    MR = cv.getPerspectiveTransform(right_last_points,new_points)
    right_img = cv.warpPerspective(in_img,MR,(out_img_shape[0],out_img_shape[1]))

    return left_img, right_img

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


# 图片矫正并保存为每个点的值
def img1points(img,pla,plb,plc,pld,atxt = "o"):
    
    img = contour_process_fa_img(img,[30,30],pla,plb,plc,pld)
    cv.imwrite('./picture/'+str(time.process_time())+'img_edge_'+atxt+'.png',img)
    hsv_img = cv.cvtColor(img,cv.COLOR_RGB2HSV)
    lab_img = cv.cvtColor(img,cv.COLOR_RGB2LAB)

    f = open('./data/hsv_points.txt',mode='a',encoding='utf-8')
    for i in range(int(hsv_img.shape[0]/6),int(hsv_img.shape[0]),int(hsv_img.shape[0]/3)):
        for j in range(int(hsv_img.shape[1]/6),int(hsv_img.shape[1]),int(hsv_img.shape[1]/3)):
            f.write(str(hsv_img[i,j][0])+'\n')
            f.write(str(hsv_img[i,j][1])+'\n')
            f.write(str(hsv_img[i,j][2])+'\n\n')
    f.close()

    f = open('./data/lab_points.txt',mode='a',encoding='utf-8')
    for i in range(int(lab_img.shape[0]/6),int(lab_img.shape[0]),int(lab_img.shape[0]/3)):
        for j in range(int(lab_img.shape[1]/6),int(lab_img.shape[1]),int(lab_img.shape[1]/3)):
            f.write(str(lab_img[i,j][0])+'\n')
            f.write(str(lab_img[i,j][1])+'\n')
            f.write(str(lab_img[i,j][2])+'\n\n')
    f.close()

# 0---1
# |   |
# 2---3
#
def imgpoints(img,atxt = "o"):
    if atxt == 1:
        #img1points(img,atxt)
        print("1")
    if atxt == 3:
        #img1points(img,atxt)
        print("3")


def img4points(img1,img2,img3,img4,atxt = "o"):
    # img1,上摄像头图片
    # img2,下摄像头图片
    # img3,前摄像头
    # img4,后摄像头
    # ##
    left_img,right_img = contour_process(img1,[30,30])
    front_img,after_img = contour_process_fa_img(img4,img3,[30,30])
    below_left_img,below_right_img = contour_below_process(img2,[30,30])
    cv.imwrite('./picture/'+str(time.process_time())+'left_img_'+atxt+'.png',left_img)
    cv.imwrite('./picture/'+str(time.process_time())+'right_img_'+atxt+'.png',right_img)
    cv.imwrite('./picture/'+str(time.process_time())+'front_img_'+atxt+'.png',front_img)
    cv.imwrite('./picture/'+str(time.process_time())+'after_img_'+atxt+'.png',after_img)
    cv.imwrite('./picture/'+str(time.process_time())+'below_left_img_'+atxt+'.png',below_left_img)
    cv.imwrite('./picture/'+str(time.process_time())+'below_right_img_'+atxt+'.png',below_right_img)

    hsv_left_img = cv.cvtColor(left_img,cv.COLOR_RGB2HSV)
    hsv_right_img = cv.cvtColor(right_img,cv.COLOR_RGB2HSV)

    lab_left_img = cv.cvtColor(left_img,cv.COLOR_RGB2LAB)
    lab_right_img = cv.cvtColor(right_img,cv.COLOR_RGB2LAB)

    hsv_front_img = cv.cvtColor(front_img,cv.COLOR_RGB2HSV)
    hsv_after_img = cv.cvtColor(after_img,cv.COLOR_RGB2HSV)

    lab_front_img = cv.cvtColor(front_img,cv.COLOR_RGB2LAB)
    lab_after_img = cv.cvtColor(after_img,cv.COLOR_RGB2LAB)

    below_hsv_left_img = cv.cvtColor(below_left_img,cv.COLOR_RGB2HSV)
    below_hsv_right_img = cv.cvtColor(below_right_img,cv.COLOR_RGB2HSV)

    below_lab_left_img = cv.cvtColor(below_left_img,cv.COLOR_RGB2LAB)
    below_lab_right_img = cv.cvtColor(below_right_img,cv.COLOR_RGB2LAB)

#上左-上右
    f = open('./data/hsv_points.txt',mode='a',encoding='utf-8')
    #上左
    for i in range(int(hsv_left_img.shape[0]/6),int(hsv_left_img.shape[0]),int(hsv_left_img.shape[0]/3)):
        for j in range(int(hsv_left_img.shape[1]/6),int(hsv_left_img.shape[1]),int(hsv_left_img.shape[1]/3)):
            f.write(str(hsv_left_img[i,j][0])+'\n')
            f.write(str(hsv_left_img[i,j][1])+'\n')
            f.write(str(hsv_left_img[i,j][2])+'\n\n')
    #上右
    for i in range(int(hsv_right_img.shape[0]/6),int(hsv_right_img.shape[0]),int(hsv_right_img.shape[0]/3)):
        for j in range(int(hsv_right_img.shape[1]/6),int(hsv_right_img.shape[1]),int(hsv_right_img.shape[1]/3)):
            f.write(str(hsv_right_img[i,j][0])+'\n')
            f.write(str(hsv_right_img[i,j][1])+'\n')
            f.write(str(hsv_right_img[i,j][2])+'\n\n')
    f.close()

    f = open('./data/lab_points.txt',mode='a',encoding='utf-8')
    #上左
    for i in range(int(lab_left_img.shape[0]/6),int(lab_left_img.shape[0]),int(lab_left_img.shape[0]/3)):
        for j in range(int(lab_left_img.shape[1]/6),int(lab_left_img.shape[1]),int(lab_left_img.shape[1]/3)):
            f.write(str(lab_left_img[i,j][0])+'\n')
            f.write(str(lab_left_img[i,j][1])+'\n')
            f.write(str(lab_left_img[i,j][2])+'\n\n')
    #上右
    for i in range(int(lab_right_img.shape[0]/6),int(lab_right_img.shape[0]),int(lab_right_img.shape[0]/3)):
        for j in range(int(lab_right_img.shape[1]/6),int(lab_right_img.shape[1]),int(lab_right_img.shape[1]/3)):
            f.write(str(lab_right_img[i,j][0])+'\n')
            f.write(str(lab_right_img[i,j][1])+'\n')
            f.write(str(lab_right_img[i,j][2])+'\n\n')
    f.close()

#下左-后
    f = open('./data/hsv_points.txt',mode='a',encoding='utf-8')
    #下左
    for i in range(int(below_hsv_left_img.shape[0]/6),int(below_hsv_left_img.shape[0]),int(below_hsv_left_img.shape[0]/3)):
        for j in range(int(below_hsv_left_img.shape[1]/6),int(below_hsv_left_img.shape[1]),int(below_hsv_left_img.shape[1]/3)):
            f.write(str(below_hsv_left_img[i,j][0])+'\n')
            f.write(str(below_hsv_left_img[i,j][1])+'\n')
            f.write(str(below_hsv_left_img[i,j][2])+'\n\n')
    #后
    for i in range(int(hsv_after_img.shape[0]/6),int(hsv_after_img.shape[0]),int(hsv_after_img.shape[0]/3)):
        for j in range(int(hsv_after_img.shape[1]/6),int(hsv_after_img.shape[1]),int(hsv_after_img.shape[1]/3)):
            f.write(str(hsv_after_img[i,j][0])+'\n')
            f.write(str(hsv_after_img[i,j][1])+'\n')
            f.write(str(hsv_after_img[i,j][2])+'\n\n')
    
    f.close()

    f = open('./data/lab_points.txt',mode='a',encoding='utf-8')
    #下左
    for i in range(int(below_lab_left_img.shape[0]/6),int(below_lab_left_img.shape[0]),int(below_lab_left_img.shape[0]/3)):
        for j in range(int(below_lab_left_img.shape[1]/6),int(below_lab_left_img.shape[1]),int(below_lab_left_img.shape[1]/3)):
            f.write(str(below_lab_left_img[i,j][0])+'\n')
            f.write(str(below_lab_left_img[i,j][1])+'\n')
            f.write(str(below_lab_left_img[i,j][2])+'\n\n')
    #后
    for i in range(int(lab_after_img.shape[0]/6),int(lab_after_img.shape[0]),int(lab_after_img.shape[0]/3)):
        for j in range(int(lab_after_img.shape[1]/6),int(lab_after_img.shape[1]),int(lab_after_img.shape[1]/3)):
            f.write(str(lab_after_img[i,j][0])+'\n')
            f.write(str(lab_after_img[i,j][1])+'\n')
            f.write(str(lab_after_img[i,j][2])+'\n\n')
    
    f.close()

#前-下右
    f = open('./data/hsv_points.txt',mode='a',encoding='utf-8')
    #前
    for i in range(int(hsv_front_img.shape[0]/6),int(hsv_front_img.shape[0]),int(hsv_front_img.shape[0]/3)):
        for j in range(int(hsv_front_img.shape[1]/6),int(hsv_front_img.shape[1]),int(hsv_front_img.shape[1]/3)):
            f.write(str(hsv_front_img[i,j][0])+'\n')
            f.write(str(hsv_front_img[i,j][1])+'\n')
            f.write(str(hsv_front_img[i,j][2])+'\n\n')
    #下右
    for i in range(int(below_hsv_right_img.shape[0]/6),int(below_hsv_right_img.shape[0]),int(below_hsv_right_img.shape[0]/3)):
        for j in range(int(below_hsv_right_img.shape[1]/6),int(below_hsv_right_img.shape[1]),int(below_hsv_right_img.shape[1]/3)):
            f.write(str(below_hsv_right_img[i,j][0])+'\n')
            f.write(str(below_hsv_right_img[i,j][1])+'\n')
            f.write(str(below_hsv_right_img[i,j][2])+'\n\n')
    f.close()

    f = open('./data/lab_points.txt',mode='a',encoding='utf-8')
    #前
    for i in range(int(lab_front_img.shape[0]/6),int(lab_front_img.shape[0]),int(lab_front_img.shape[0]/3)):
        for j in range(int(lab_front_img.shape[1]/6),int(lab_front_img.shape[1]),int(lab_front_img.shape[1]/3)):
            f.write(str(lab_front_img[i,j][0])+'\n')
            f.write(str(lab_front_img[i,j][1])+'\n')
            f.write(str(lab_front_img[i,j][2])+'\n\n')
    #下右
    for i in range(int(below_lab_right_img.shape[0]/6),int(below_lab_right_img.shape[0]),int(below_lab_right_img.shape[0]/3)):
        for j in range(int(below_lab_right_img.shape[1]/6),int(below_lab_right_img.shape[1]),int(below_lab_right_img.shape[1]/3)):
            f.write(str(below_lab_right_img[i,j][0])+'\n')
            f.write(str(below_lab_right_img[i,j][1])+'\n')
            f.write(str(below_lab_right_img[i,j][2])+'\n\n')
    f.close()