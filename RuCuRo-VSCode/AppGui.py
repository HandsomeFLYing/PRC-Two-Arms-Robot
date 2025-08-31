import tkinter as tk
import threading
import serial
import serial.tools.list_ports
import cv2 as cv
from PIL import Image,ImageTk
import os
import shutil
import time
from tkinter import ttk
from tkinter import messagebox

import datetime
import cube
from cube import points_list
import solution
#import kmeans
import ser
#备份数据
import DataBackup
Backuo = DataBackup.Backuo()

# 获取可用串口
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
#相机配置
exposure = -5
camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv.CAP_PROP_EXPOSURE, exposure)

# 显示图像更新
def video_loop():
    ret, img = camera.read()  # 从摄像头读取照片
    img = cv.flip(img, 1)
    if ret:
        img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
        # 画魔方轮廓线
        cv.line(img,points_list[0],points_list[1],(0,255,0),3),cv.line(img,points_list[1],points_list[2],(0,255,0),3)
        cv.line(img,points_list[2],points_list[3],(0,255,0),3),cv.line(img,points_list[3],points_list[4],(0,255,0),3)
        cv.line(img,points_list[4],points_list[5],(0,255,0),3),cv.line(img,points_list[5],points_list[0],(0,255,0),3)
        cv.line(img,points_list[1],points_list[4],(0,255,0),3)
        cv.line(img,(40,300),(440,300),(100,255,0),3)
        cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        cube_panel.imgtk = imgtk
        cube_panel.config(image=imgtk)

        window.after(50, video_loop)

# 绘画六面颜色
import cube_from_list
def draw_cube_ja():
    cube_from_list.draw_cube_ja(window)
def draw_cube():
    cube_from_list.draw_cube(window)


# 处理结果并输出
def check_data_su():
    cube_from_list.result_lb(window,"处理数据中...")
    for n in range(30):
        #print('（1-推算？）')
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
                messagebox.showinfo("成功推算","已有结果(检查机器状态是否良好)")
                if CAMARA:
                    ser.ser_send(send_string[0:64])
                    print(send_string[0:64])
                    t1 = time.process_time()
                    while(time.process_time()<t1+2):pass
                    ser.ser_send(send_string[64:])
                    ser.ser_send(b'c')
                    
                cube_from_list.result_lb(window,print_str)
                print("发生结果？")
                break
            else:
                color = ['white','red','green','yellow','orange','blue']
                for i in range(6):
                    if os.path.exists('data/sort.txt'):
                        os.remove('data/sort.txt')
                    if os.path.exists('data/'+color[i]+'.txt'):
                        os.remove('data/'+color[i]+'.txt')
                print("异常的无结？")
    print("CC-处理结束")

def draw_result():
    print(time.process_time())
    if CAMARA:
        global camera
        if camera.isOpened():
            camera.release()
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
    if not camera.isOpened():
        camera = cv.VideoCapture(0)
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
def save_picture():
    cube_from_list.result_lb(window,"拍摄系统启动")
    print("（图像处理 ：）启动")
    if not CAMARA_1:
        print("（图像处理 ：）模拟1")
        img = cv.imread('test/20250625_175347/5.734375.png')
        cube.img2points(img,"1")
        print("（图像处理 ：）模拟2")
        img = cv.imread('test/20250625_175347/7.546875.png')
        cube.img2points(img,"2")
        print("（图像处理 ：）模拟3")
        img = cv.imread('test/20250625_175347/9.359375.png')
        cube.img2points(img,"3")

    if CAMARA_1:   
        for i in range(3):
            print("（图像处理 ：）Pi"+str(i)+"\t"+str(time.process_time()))
            camera = cv.VideoCapture(0)
            ret, img = camera.read()
            img = cv.flip(img, 1)
            img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
            camera.release()
            # 增加曝光（亮度调整）
            #alpha = 2.0  # 对比度
            #beta = 0    # 亮度增加值
            #brightened_img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
            cube.img2points(img,str(i))
            cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
            ser.ser_send(b'XzC')
            if(i<2):
                t0 = time.process_time()
                while(time.process_time()<t0+delay_time):
                    pass
        if(False):
            camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
            camera.set(cv.CAP_PROP_EXPOSURE, exposure)
            camera.set(cv.CAP_PROP_EXPOSURE, exposure)
    #time.sleep(4)
    cube_from_list.result_lb(window,"拍摄完成")

#单独拍摄
def cube_cv_img():
    global camera
    if camera.isOpened():
        camera.release()
    global img_su
    print("（图像处理 ：）Pi"+str(img_su.get())+"\t"+str(time.process_time()))
    camera = cv.VideoCapture(0)
    ret, img = camera.read()
    img = cv.flip(img, 1)
    img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
    camera.release()
    # 增加曝光（亮度调整）
            #alpha = 2.0  # 对比度
            #beta = 0    # 亮度增加值
            #brightened_img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    cube.img2points(img,str(img_su.get()))
    cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
    if not camera.isOpened():
        camera = cv.VideoCapture(0)
    
    
        
#切换连接设备
def on_confirm():
    on_combobox,on_baudrate = port_combobox.get(),int(baudrate_combobox.get())
    try:
        #串口重连  
        ser.connect_to_arduino(on_combobox,on_baudrate, 1, False)
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
        global camera
        if not camera.isOpened():
            camera = cv.VideoCapture(0)
    Backuo
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
window.geometry("1340x760")

#调用摄像头
if CAMARA:
    ser.ser_init()
    cube_panel = tk.Label(window)
    cube_panel.place(x = 20,y = 20)
    video_loop()

draw_cube()

x1_x,y1_y = 520 , 400
#工作按钮
run_btn = tk.Button(window,
    text='全自动还原',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=draw_result) 
run_btn.place(x = x1_x,y = y1_y +120)
#开关爪
zhua_no_btn = tk.Button(window,text='开爪',
                        width=12, height=2,font=('Arial', 12),bg = 'Yellow',
                        command=zhua_result_on) 
zhua_no_btn.place(x = x1_x,y = y1_y)    
zhua_off_btn = tk.Button(window,text='合爪',
                        width=12, height=2,font=('Arial', 12),bg = 'Yellow',
                        command=zhua_result_off)   
zhua_off_btn.place(x = x1_x,y = y1_y +60)    


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


#手动处理按键
img_label = tk.Label(window, text="编号：",width=6,font=('Arial', 14))
img_label.place(x = 510,y = 300)
var1 = tk.IntVar()
var1.set(1)
img_su = tk.Spinbox(window,
    from_=0, to=99,
    width=4, increment=2,
    font=('Arial', 16),
    textvariable=var1)
img_su.place(x = 580,y = 300)
cube_cv_btn = tk.Button(window,
    text='手动拍摄处理',width=15, 
    font=('Arial', 12),bg = "#ffba30",
    command=cube_cv_img) 
cube_cv_btn.place(x = 650,y = 298) 
check_data_su_btn = tk.Button(window,
    text='处理现成数据',width=14, 
    font=('Arial', 12),bg = '#ffba30',
    command=check_data_su) 
check_data_su_btn.place(x = 800,y = 298)




#状态显示框
cube_from_list.result_lb(window,"等待就绪")

#速度调整拦
speed_lb = tk.Label(window,text='速度：',width=6,font=('Arial', 14))
speed_lb.place(x = 510,y = 260)
var = tk.IntVar()
var.set(30)
speed_spin = tk.Spinbox(window,
    from_=0, to=99,
    width=4, increment=2,
    font=('Arial', 16),
    textvariable=var)
speed_spin.place(x = 580,y = 260)
speed_btn = tk.Button(window,
    text='上传速度',width=15,
    font=('Arial', 12),bg = "#00F2FF",
    command=speed_sc) 
speed_btn.place(x = 650,y = 258) 





#命令栏
def ser_input():
    text = f"b'{entry.get()}'"  # 获取输入框文本
    send_string = text.encode('utf-8')
    print(f"上传命令: {text}")
    ser.ser_send(send_string[0:64])
    # 可选：清空输入框
    entry.delete(0, tk.END)
entry = tk.Entry(window,font=("Arial", 14),  # 字体和大小
    width=25,bd=2  # 输入框宽度# 边框宽度
    )
entry.place(x = 510,y = 220)  
button_cmd = tk.Button(window,
    text="上传命令",font=("Arial", 12),
    bg="lightblue",width=14,
    command=ser_input
    )
button_cmd.place(x = 800,y = 218)
help_btn = tk.Button(window,
    text='帮助',width=14,
    font=('Arial', 12),bg="#FFC36A",
    command=lambda: ser.show_help(messagebox)) 
help_btn.place(x = 940,y = 218) 



#串口修改器窗口
serial_port_x = 0.8
    # 串口选择下拉框
port_label = tk.Label(window, text="选择串口:")
port_label.place(x = 1080,y = 218)
port_combobox = ttk.Combobox(window, values=available_ports)
if available_ports:
    port_combobox.set(available_ports[0])
port_combobox.place(x = 1080,y = 248)
# 波特率选择下拉框
baudrates = [5200, 9600, 115200, 230400]
baudrate_label = tk.Label(window, text="选择波特率:")
baudrate_label.place(x = 1080,y = 278)
baudrate_combobox = ttk.Combobox(window, values=baudrates)
baudrate_combobox.set(115200)
baudrate_combobox.place(x = 1080,y = 308)
# 切换设备按钮
confirm_button = tk.Button(window, 
    text="尝试切换链接",width=16,
    font=('Arial', 12),bg = "#FF4AF0",
    command=on_confirm
)
confirm_button.place(x = 1080,y = 378)
break_com_btn = tk.Button(window,
    text='断开连接设备',width=16,
    font=('Arial', 12),bg="#FFC36A",
    command=lambda: ser.connect_to_arduino(disconnect=True)) 
break_com_btn.place(x = 1080,y = 338) 


window.mainloop()

# 当一切都完成后，关闭摄像头并释放所占资源
if CAMARA:
    camera.release()
    ser.ser_close()
cv.destroyAllWindows()