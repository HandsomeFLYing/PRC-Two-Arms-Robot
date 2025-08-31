import tkinter as tk
import threading
import serial
import serial.tools.list_ports
import cv2 as cv
from PIL import Image, ImageTk
import os
import shutil
import time
from tkinter import ttk
from tkinter import messagebox
import logging
import datetime
import cube
from ImgHD import points_list
from ImgHD import points_list_cv1
from ImgHD import points_list_cv2
import solution
#import kmeans
import ser
#备份数据
import DataBackup
Backuo = DataBackup.Backuo()

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

### 新增：检测可用摄像头
def detect_available_cameras(max_id=10):
    """检测系统中实际可用的摄像头ID"""
    available = []
    for i in range(max_id):
        cap = cv.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

### 获取可用串口
def list_com_ports():
    """列出电脑上所有可用的 COM 端口"""
    ports = serial.tools.list_ports.comports()
    com_ports = []
    for port, desc, hwid in sorted(ports):
        com_ports.append(port)
    return com_ports

arduino_ser = None
available_ports = list_com_ports()

###程序开关
#串口开关（0关1开）//这里关闭将停止大部分功能
CAMARA = 1
#模型摄像头开关 //传递依然继续
CAMARA_1 = 1

###相机
#拍照间隔
delay_time = 1.8

### 相机配置
# 检测实际可用的摄像头
available_cameras = detect_available_cameras()
logging.info(f"检测到可用摄像头ID: {available_cameras}")

# 初始化4个摄像头（若可用）
cameras = [None] * 4
for i in range(4):
    if i in available_cameras:#True:#
        try:
            # 相机配置
            exposure = -5
            cameras[i] = cv.VideoCapture(i)
            cameras[i].set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
            cameras[i].set(cv.CAP_PROP_EXPOSURE, exposure)
            cameras[i].set(cv.CAP_PROP_FPS, 30)  # 降低帧率
            #cameras[i].set(cv.CAP_PROP_FRAME_WIDTH, 640)  # 降低宽度
            #cameras[i].set(cv.CAP_PROP_FRAME_HEIGHT, 480) # 降低高度
            logging.info(f"成功初始化摄像头 {i}")
        except Exception as e:
            logging.error(f"初始化摄像头 {i} 失败: {str(e)}")
            cameras[i] = None
    else:
        logging.warning(f"摄像头 {i} 未检测到")

# 显示图像更新
def video_loop_0():
    if cameras[0] is None:
        window.after(50, video_loop_0)
        return
    
    ret, img = cameras[0].read()  # 从摄像头0读取
    if ret:
        img = cv.flip(img, 1)
        img = cv.resize(img, (480, 360), interpolation=cv.INTER_CUBIC)
        # 画魔方轮廓线
        cv.line(img, points_list[0], points_list[1], (0, 255, 0), 3), cv.line(img, points_list[1], points_list[2], (0, 255, 0), 3)
        cv.line(img, points_list[2], points_list[3], (0, 255, 0), 3), cv.line(img, points_list[3], points_list[4], (0, 255, 0), 3)
        cv.line(img, points_list[4], points_list[5], (0, 255, 0), 3), cv.line(img, points_list[5], points_list[0], (0, 255, 0), 3)
        cv.line(img, points_list[1], points_list[4], (0, 255, 0), 3)
        cv.line(img, (40, 300), (440, 300), (100, 255, 0), 3)
        
        cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        cube_panel_0.imgtk = imgtk
        cube_panel_0.config(image=imgtk)
    
    window.after(50, video_loop_0)

def video_loop_1():
    if cameras[1] is None:
        window.after(50, video_loop_1)
        return
    
    ret, img = cameras[1].read()  # 从摄像头1读取
    if ret:
        img = cv.flip(img, 1)
        img = cv.resize(img, (480, 360), interpolation=cv.INTER_CUBIC)
        # 画魔方轮廓线
        cv.line(img, points_list_cv1[0], points_list_cv1[1], (0, 255, 0), 3)#, cv.line(img, points_list[1], points_list[2], (0, 255, 0), 3)
        #cv.line(img, points_list[2], points_list[3], (0, 255, 0), 3), cv.line(img, points_list[3], points_list[4], (0, 255, 0), 3)
        cv.line(img, points_list_cv1[3], points_list_cv1[2], (0, 255, 0), 3), cv.line(img, points_list_cv1[2], points_list_cv1[0], (0, 255, 0), 3)
        cv.line(img, points_list_cv1[1], points_list_cv1[3], (0, 255, 0), 3)
        #cv.line(img, (40, 300), (440, 300), (100, 255, 0), 3)
        
        cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)
        current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=current_image)
        cube_panel_1.imgtk = imgtk
        cube_panel_1.config(image=imgtk)
    
    window.after(50, video_loop_1)

def video_loop_2():
    if cameras[2] is None:
        window.after(50, video_loop_2)
        return
    
    ret, img = cameras[2].read()  # 从摄像头2读取
    if ret:
        img = cv.flip(img, 1)
        img = cv.resize(img, (480, 360), interpolation=cv.INTER_CUBIC)
        # 画魔方轮廓线
        cv.line(img, points_list_cv2[0], points_list_cv2[1], (0, 255, 0), 3), cv.line(img, points_list_cv2[1], points_list_cv2[3], (0, 255, 0), 3)
        cv.line(img, points_list_cv2[3], points_list_cv2[2], (0, 255, 0), 3), cv.line(img, points_list_cv2[2], points_list_cv2[0], (0, 255, 0), 3)
        cv.line(img, points_list_cv2[4], points_list_cv2[5], (0, 255, 0), 3), cv.line(img, points_list_cv2[5], points_list_cv2[7], (0, 255, 0), 3)
        cv.line(img, points_list_cv2[7], points_list_cv2[6], (0, 255, 0), 3), cv.line(img, points_list_cv2[6], points_list_cv2[4], (0, 255, 0), 3)
        #cv.line(img, (40, 300), (440, 300), (100, 255, 0), 3)
        
        cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)
        current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=current_image)
        cube_panel_2.imgtk = imgtk
        cube_panel_2.config(image=imgtk)
    
    window.after(50, video_loop_2)

def video_loop_3():
    if cameras[3] is None:
        window.after(50, video_loop_3)
        return
    
    ret, img = cameras[3].read()  # 从摄像头3读取
    if ret:
        img = cv.flip(img, 1)
        img = cv.resize(img, (480, 360), interpolation=cv.INTER_CUBIC)
        # 画魔方轮廓线
        #cv.line(img, points_list[0], points_list[1], (0, 255, 0), 3),
        cv.line(img, points_list_cv1[4], points_list_cv1[5], (0, 255, 0), 3)
        cv.line(img, points_list_cv1[5], points_list_cv1[7], (0, 255, 0), 3), cv.line(img, points_list_cv1[6], points_list_cv1[4], (0, 255, 0), 3)
        #cv.line(img, points_list[4], points_list[5], (0, 255, 0), 3), cv.line(img, points_list[5], points_list[0], (0, 255, 0), 3)
        cv.line(img, points_list_cv1[6], points_list_cv1[7], (0, 255, 0), 3)
        #cv.line(img, (40, 300), (440, 300), (100, 255, 0), 3)
        
        cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)
        current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=current_image)
        cube_panel_3.imgtk = imgtk
        cube_panel_3.config(image=imgtk)
    
    window.after(50, video_loop_3)

# 绘画六面颜色
import cube_from_list
cube_from_list.draw_cube_x = 985
cube_from_list.draw_cube_y = 20
def draw_cube_ja():
    cube_from_list.draw_cube_ja(window)
def draw_cube():
    cube_from_list.draw_cube(window)

# 处理结果并输出
def check_data_su():
    cube_from_list.result_lb(window,"处理数据中...")
    for n in range(30):
        print('（1-推算？）')
        #time.sleep(0.1)
        if(n%2==0):
            gamut_type = 'hsv'
        else:
            gamut_type = 'lab'
        points,label,center,color_dict = cube.kmeans(gamut_type)
        if(cube.check_data() == 1):
            cube.cube_list_sort()
            code_str = solution.code2str()
            step_str,print_str = solution.str2step(code_str)
            send_string = step_str.encode('utf-8')
            if not(len(step_str) == 0):
                print(n)
                #cube.plot(points,label,center,color_dict)#可视化
                draw_cube()
                #messagebox.showinfo("成功推算","已有结果(检查机器状态是否良好)")
                if CAMARA:
                    ser.ser_send(send_string[0:64])
                    print(send_string[0:64])
                    t1 = time.process_time()
                    while(time.process_time()<t1+2):pass
                    ser.ser_send(send_string[64:])
                    ser.ser_send(b'c')                    
                cube_from_list.result_lb(window,print_str)
                print("发生结果？")
                return
            else:
                color = ['white','red','green','yellow','orange','blue']
                for i in range(6):
                    if os.path.exists('data/sort.txt'):
                        os.remove('data/sort.txt')
                    if os.path.exists('data/'+color[i]+'.txt'):
                        os.remove('data/'+color[i]+'.txt')
                print("异常的无结？")
    cube_from_list.result_lb(window,"数据处理结束")
    print("CC-处理结束")

def draw_result():
    reset()
    print(time.process_time())
    if CAMARA:
        if CAMARA_1:
            for i in range(4):
                global camera0
                camera0 = cameras[i]
                if camera0.isOpened():
                    camera0.release()
        global speed_spin
        print(speed_spin.get())

        speed_str = 'S'
        speed_str += str(speed_spin.get())
        speed_byte  =  speed_str.encode('utf-8')
        ser.ser_send(speed_byte)
        print(speed_byte)
        #上传
        ser.ser_send(b'l')
    
    save_picture()
    if CAMARA_1:
        for i in range(4):
            camera0 = cameras[i]
            if not camera0.isOpened():
                cameras[i] = cv.VideoCapture(i)
    check_data_su()

def speed_sc():
    if CAMARA:
        global speed_spin
        print(speed_spin.get())
        speed_str = 'S'
        speed_str += str(speed_spin.get())
        speed_byte  =  speed_str.encode('utf-8')
        ser.ser_send(speed_byte)
        ser.ser_send(b'l')
        print("（速度）:"+ str(speed_byte))
                
#开合机械爪
def zhua_result_on():#k
   if CAMARA:
        ser.ser_send(b'e')
        print("（zhua）尝试状态：on")

def zhua_result_off():#g
   if CAMARA:
        ser.ser_send(b'l')
        print("（zhua）尝试状态：off")
    

# 截图保存图片并处理成数据
import ImgHD
def save_picture():
    img_cun = [None] * 4
    cube_from_list.result_lb(window,"拍摄系统启动")
    print("（图像处理 ：）启动")
    if not CAMARA_1:
        img_cun[0] = cv.imread('test/20250627_192538/50.015625.png') #上·0
        img_cun[1] = cv.imread('test/20250627_192538/53.734375.png') #后·1
        img_cun[2] = cv.imread('test/20250627_192538/53.71875.png') #下·2
        img_cun[3] = cv.imread('test/20250627_192538/51.890625.png') #前·1
        print("（图像处理 ：）模拟模式")
        ImgHD.img4points(img_cun[0],img_cun[2],img_cun[1],img_cun[3])

    if CAMARA_1:
        
        for i in range(4):
            print("（图像处理 ：）Pi"+str(i)+"\t"+str(time.process_time()))
            camera = cv.VideoCapture(i)
            ret, img = camera.read()
            img = cv.flip(img, 1)
            img_cun[i] = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
            camera.release()
            # 增加曝光（亮度调整）
            #alpha = 2.0  # 对比度
            #beta = 0    # 亮度增加值
            #brightened_img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
            cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
            #ser.ser_send(b'XzC')
            if(i<2):
                t0 = time.process_time()
                while(time.process_time()<t0+delay_time):
                    pass 
        ImgHD.img4points(img_cun[0],img_cun[2],img_cun[1],img_cun[3])
        #处理拍照数据

         
        """for i in range(4):
            print("（图像处理 ：）Pi"+str(i)+"\t"+str(time.process_time()))
            # 修正：使用 cameras[i] 而不是重新创建 VideoCapture
            if cameras[i] is not None:
                ret, img = cameras[i].read()
                if ret:
                    print("拍照")
                    img = cv.flip(img, 1)
                    img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
                    if i== 0:cube.img2points(img,str(i))
                    if i== 1:ImgHD.imgpoints(img,str(i))
                    if i== 2:cube.img2points(img,str(i))
                    if i== 3:ImgHD.imgpoints(img,str(i))
                    
                    cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
                    #ser.ser_send(b'XzC')
                    if(i<2):
                        t0 = time.process_time()
                        while(time.process_time()<t0+delay_time):
                            pass
            else:
                logging.error(f"摄像头 {i} 不可用，跳过拍摄")
                messagebox.showerror("错误", f"摄像头 {i} 不可用，请检查连接")
                return
               """ 
    cube_from_list.result_lb(window,"拍摄完成")

#单独拍摄
def cube_cv_img():
    for i in range(4):
        global camera0
        camera0 = cameras[i]
        if camera0.isOpened():
            camera0.release()
    img_cun = [None] * 4
    cube_from_list.result_lb(window,"拍摄系统启动")
    for i in range(4):
        print("（图像处理 ：）Pi"+str(i)+"\t"+str(time.process_time()))
        camera = cv.VideoCapture(i)
        ret, img = camera.read()
        img = cv.flip(img, 1)
        img_cun[i] = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
        camera.release()
            # 增加曝光（亮度调整）
            #alpha = 2.0  # 对比度
            #beta = 0    # 亮度增加值
            #brightened_img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
        cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
            #ser.ser_send(b'XzC')
        if(i<2):
            t0 = time.process_time()
            while(time.process_time()<t0+delay_time):
                pass 
    ImgHD.img4points(img_cun[0],img_cun[2],img_cun[1],img_cun[3])
    for i in range(4):
        camera0 = cameras[i]
        if not camera0.isOpened():
            cameras[i] = cv.VideoCapture(i)
    
        
#切换连接设备
def on_confirm():
    on_combobox,on_baudrate = port_combobox.get(),int(baudrate_combobox.get())
    try:
        #串口重连  
        ser.connect_to_arduino(on_combobox,on_baudrate, 1, False,cube_from_list.result_lb,window)
        #print("（GUI 212）设备发生了一次变动？")
        ser.ser_init()
    except serial.SerialException as e:
        print(f"（GUI 212）尝试切换异常 ,错误原因on_confirm)  {e}")
def refresh_ports():
    available_ports = list_com_ports()
    port_combobox['values'] = available_ports
    if available_ports:
        port_combobox.set(available_ports[0])
    window.after(2000, refresh_ports)        
        
        
#重置程序
def reset():
    if CAMARA:
        ser.ser_send(b'c')
        # 修正：检查 cameras[0] 而不是 camera0
        if cameras[0] is not None and not cameras[0].isOpened():
            cameras[0] = cv.VideoCapture(0)
            cameras[0].set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
            cameras[0].set(cv.CAP_PROP_EXPOSURE, -5)
    DataBackup.Backuo()
    shutil.rmtree('./data')
    os.mkdir('./data')
    shutil.rmtree('./picture')
    os.mkdir('./picture')
    draw_cube()
    cube_from_list.result_lb(window,"")
    cube_from_list.result_lb(window,"重置成功等待。。。")
    print("（reset）重置成功")


#初始化缓存文件
if(True):
    if (os.path.exists('./data')):
        shutil.rmtree('./data')
    os.mkdir('./data')
    if (os.path.exists('./picture')):
        shutil.rmtree('./picture')
    os.mkdir('./picture')


#创建窗口对象
window = tk.Tk()
window.title("湖州职业技术学院")
window.geometry("1920x1080")

#调用摄像头
if CAMARA:
    ser.ser_init()
    cube_panel_0 = tk.Label(window)
    cube_panel_0.place(x = 20,y = 20)
    if cameras[0] is not None:
        video_loop_0()
    else:
        cube_panel_0.config(text="摄像头0未检测到", font=("Arial", 16), fg="red")
    
    cube_panel_1 = tk.Label(window)
    cube_panel_1.place(x = 500,y = 20)
    if cameras[1] is not None:
        video_loop_1()
    else:
        cube_panel_1.config(text="摄像头1未检测到", font=("Arial", 16), fg="red")
    
    cube_panel_2 = tk.Label(window)
    cube_panel_2.place(x = 20,y = 380)
    if cameras[2] is not None:
        video_loop_2()
    else:
        cube_panel_2.config(text="摄像头2未检测到", font=("Arial", 16), fg="red")
    
    cube_panel_3 = tk.Label(window)
    cube_panel_3.place(x = 500,y = 380)
    if cameras[3] is not None:
        video_loop_3()
    else:
        cube_panel_3.config(text="摄像头3未检测到", font=("Arial", 16), fg="red")

draw_cube()

x1_x,y1_y = 990 , 400
#工作按钮
run_btn = tk.Button(window,
    text='全自动还原',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=draw_result) 
run_btn.place(x = x1_x,y = y1_y +120)

run_btn2 = tk.Button(window,
    text='开始',      
    width=12, height=2,
    font=('Arial', 46),bg = "#C636FF",
    command=draw_result) 
run_btn2.place(x = x1_x,y = y1_y +180)


#开关爪
zhua_no_btn = tk.Button(window,text='开爪',
                        width=12, height=2,font=('Arial', 12),bg = 'Yellow',
                        command=zhua_result_on) 
zhua_no_btn.place(x = x1_x,y = y1_y)    
zhua_off_btn = tk.Button(window,text='合爪',
                        width=12, height=2,font=('Arial', 12),bg = 'Yellow',
                        command=zhua_result_off)   
zhua_off_btn.place(x = x1_x,y = y1_y +60)    

#其他按钮
draw_cube_btn = tk.Button(window,
    text='绘图',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=draw_cube) 
draw_cube_btn.place(x = x1_x+120,y = y1_y)
draw_cube_jb_btn = tk.Button(window,
    text='识别绘图',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=draw_cube_ja) 
draw_cube_jb_btn.place(x = x1_x+120,y = y1_y +60) 
picture_btn = tk.Button(window,
    text='重置程序',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=reset) 
picture_btn.place(x = x1_x+120,y = y1_y +120)

#命令区
ser_input_x , ser_input_y = 980,780
#手动处理按键
img_label = tk.Label(window, text="编号：",width=6,font=('Arial', 14))
img_label.place(x = ser_input_x,y = ser_input_y+80)
var1 = tk.IntVar()
var1.set(1)
img_su = tk.Spinbox(window,
    from_=0, to=99,
    width=4, increment=2,
    font=('Arial', 16),
    textvariable=var1)
img_su.place(x = ser_input_x +70 ,y = ser_input_y+80)
cube_cv_btn = tk.Button(window,
    text='手动拍摄处理',width=15, 
    font=('Arial', 12),bg = "#ffba30",
    command=cube_cv_img) 
cube_cv_btn.place(x = ser_input_x +140,y = ser_input_y+78) 
check_data_su_btn = tk.Button(window,
    text='处理现成数据',width=14, 
    font=('Arial', 12),bg = '#ffba30',
    command=check_data_su) 
check_data_su_btn.place(x = ser_input_x +290,y = ser_input_y+78)

#状态显示框
cube_from_list.result_lb_x , cube_from_list.result_lb_y = 20 , 760
cube_from_list.result_lb(window,"等待就绪")

#命令栏
def ser_input():
    text = f"b'{entry.get()}'"  # 获取输入框文本
    send_string = text.encode('utf-8')
    print(f"上传命令: {text}")
    cube_from_list.result_lb(window,f"打包上传命令: {text}")
    if ser.ser_send(send_string[0:64]):
        cube_from_list.result_lb(window,f"成功上传命令: {text}")
    else:cube_from_list.result_lb(window,f"上传失败！！\n {text}")
    # 可选：清空输入框
    entry.delete(0, tk.END)
entry = tk.Entry(window,font=("Arial", 14),  # 字体和大小
    width=25,bd=2  # 输入框宽度# 边框宽度
    )
entry.place(x = ser_input_x ,y = ser_input_y)  
button_cmd = tk.Button(window,
    text="上传命令",font=("Arial", 12),
    bg="lightblue",width=14,
    command=ser_input
    )
button_cmd.place(x = ser_input_x +290 ,y = ser_input_y-2)
help_btn = tk.Button(window,
    text='帮助',width=14,
    font=('Arial', 12),bg="#FFC36A",
    command=lambda: ser.show_help(messagebox)) 
help_btn.place(x = ser_input_x +430 ,y = ser_input_y-2) 

#速度调整拦
speed_lb = tk.Label(window,text='速度：',width=6,font=('Arial', 14))
speed_lb.place(x = ser_input_x ,y = ser_input_y+40)
var = tk.IntVar()
var.set(30)
speed_spin = tk.Spinbox(window,
    from_=0, to=99,
    width=4, increment=2,
    font=('Arial', 16),
    textvariable=var)
speed_spin.place(x = ser_input_x +70,y = ser_input_y +40)
speed_btn = tk.Button(window,
    text='上传速度',width=15,
    font=('Arial', 12),bg = "#00F2FF",
    command=speed_sc) 
speed_btn.place(x = ser_input_x +140,y = ser_input_y+40) 

#串口修改器窗口
serial_port_x,serial_port_y= 1480,400
# 串口选择下拉框
port_label = tk.Label(window, text="选择串口:")
port_label.place(x = serial_port_x,y = serial_port_y)
port_combobox = ttk.Combobox(window, values=available_ports)
if available_ports:
    port_combobox.set(available_ports[0])
port_combobox.place(x = serial_port_x,y = serial_port_y+30)
# 波特率选择下拉框
baudrates = [5200, 9600, 115200, 230400]
baudrate_label = tk.Label(window, text="选择波特率:")
baudrate_label.place(x = serial_port_x,y = serial_port_y+60)
baudrate_combobox = ttk.Combobox(window, values=baudrates)
baudrate_combobox.set(115200)
baudrate_combobox.place(x = serial_port_x,y = serial_port_y+90)
# 切换设备按钮
confirm_button = tk.Button(window, 
    text="尝试切换链接",width=16,
    font=('Arial', 12),bg = "#FF4AF0",
    command=on_confirm
)
confirm_button.place(x = serial_port_x,y = serial_port_y+160)
break_com_btn = tk.Button(window,
    text='断开连接设备',width=16,
    font=('Arial', 12),bg="#FFC36A",
    command=lambda: ser.connect_to_arduino(disconnect=True,result_lb = cube_from_list.result_lb,window = window)) 
break_com_btn.place(x = serial_port_x,y = serial_port_y+120) 

window.mainloop()

# 当一切都完成后，关闭摄像头并释放所占资源
if CAMARA:
    for i in range(4):
        if cameras[i] is not None:
            cameras[i].release()
    ser.ser_close()
cv.destroyAllWindows()