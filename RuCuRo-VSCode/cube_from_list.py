
import serial
import serial.tools.list_ports
import ser
import tkinter as tk
import os
from tkinter import ttk


"""
def list_com_ports():
    #列出电脑上所有可用的 COM 端口
    ports = serial.tools.list_ports.comports()
    com_ports = []
    for port, desc, hwid in sorted(ports):
        com_ports.append(port)
    return com_ports
arduino_ser = None
    # 获取可用串口
available_ports = list_com_ports()
baudrates = [5200, 9600, 115200, 230400]
def window_tk(window):
    return ttk.Combobox(window, values=available_ports),ttk.Combobox(window, values=baudrates)
#切换连接设备
def on_confirm(window):
    port_combobox , baudrate_combobox = window_tk(window)
    on_combobox,on_baudrate = port_combobox.get(),int(baudrate_combobox.get())
    try:
        #串口重连  
        ser.arduino_ser = serial.Serial(on_combobox,on_baudrate)
        print("（GUI 212）设备发生了一次变动？")
        ser.ser_init()
    except serial.SerialException as e:
        print(f"（GUI 212）尝试切换异常 ,错误原因on_confirm)  {e}")
def refresh_ports(window):
    port_combobox , baudrate_combobox = window_tk(window)
    available_ports = list_com_ports()
    port_combobox['values'] = available_ports
    if available_ports:
        port_combobox.set(available_ports[0])
    window.after(2000, refresh_ports(window))        

def from_com_list(window):
    window_tk(window)
    #串口修改器窗口
    serial_port_x = 0.8
        # 串口选择下拉框
    port_label = tk.Label(window, text="选择串口:")
    port_label.place(relx = serial_port_x,rely = 0.6)
    port_combobox = ttk.Combobox(window, values=available_ports)
    if available_ports:
        port_combobox.set(available_ports[0])
    port_combobox.place(relx = serial_port_x,rely = 0.62)
        # 波特率选择下拉框
    baudrate_label = tk.Label(window, text="选择波特率:")
    baudrate_label.place(relx = serial_port_x,rely = 0.68)
    baudrate_combobox = ttk.Combobox(window, values=baudrates)
    baudrate_combobox.set(115200)
    baudrate_combobox.place(relx = serial_port_x,rely = 0.70)
        # 切换设备按钮
    confirm_button = tk.Button(window, 
        text="尝试切换链接",
        width=16, height=2,
        font=('Arial', 12),bg = 'Pink',
        command=on_confirm(window)
    )
    confirm_button.place(relx = serial_port_x,rely = 0.78)
"""

#魔方六面绘画
color = ['green','red','orange','white','yellow','blue']
color_ = ['g','r','o','w','y','b']
draw_cube_x, draw_cube_y = 20,380
def draw_cube_ja(window):
    
    # 创建画布
    canvas = tk.Canvas(window,width=480,height=360,bg="#FA9FFF")
    for n in range(len(color)):
        col = row = 0
        if (color[n] == 'white'):
            col = 1
            row = 0
        elif (color[n] == 'orange'):
            col = 0
            row = 1
        elif (color[n] == 'green'):
            col = 1
            row = 1
        elif (color[n] == 'red'):
            col = 2
            row = 1
        elif (color[n] == 'blue'):
            col = 3
            row = 1
        elif (color[n] == 'yellow'):
            col = 1
            row = 2
    

        x=10+col*120;y=10+row*120
        if(os.path.exists('data/'+color_[n]+'.txt')):
            if(os.path.exists('data/'+color_[n]+'.txt')):
                f = open('data/'+color_[n]+'.txt',mode='r',encoding='utf-8')
            else:
                f = open('data/'+color_[n]+'.txt')
            color_list = []
            for line in f.readlines(): #依次读取每行
                color_list.append(line.strip()) #去掉每行头尾空白
            f.close()

            if (len(color_list)==9):
                for i in range(3):
                    for j in range(3):
                        #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                        canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill=str(color_list[i+j*3]),outline='black')
        else:
            for i in range(3):
                for j in range(3):
                    #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                    canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill='pink',outline='black')
    canvas.pack()#包装画布
    #魔方面位置
    canvas.place(x=draw_cube_x, y=draw_cube_y)
    print("（G ja0）已经生成扫描后的魔方状态？")

def draw_cube(window):
    # 创建画布
    canvas = tk.Canvas(window,width=480,height=360,bg="pink")
    for n in range(len(color)):
        col = row = 0
        if (color[n] == 'white'):
            col = 1
            row = 0
        elif (color[n] == 'orange'):
            col = 0
            row = 1
        elif (color[n] == 'green'):
            col = 1
            row = 1
        elif (color[n] == 'red'):
            col = 2
            row = 1
        elif (color[n] == 'blue'):
            col = 3
            row = 1
        elif (color[n] == 'yellow'):
            col = 1
            row = 2

        x=10+col*120;y=10+row*120
        if(os.path.exists('data/'+color[n]+'.txt')):
            if(os.path.exists('data/'+color_[n]+'.txt')):
                f = open('data/'+color_[n]+'.txt',mode='r',encoding='utf-8')
            else:
                f = open('data/'+color[n]+'.txt')
            color_list = []
            for line in f.readlines(): #依次读取每行
                color_list.append(line.strip()) #去掉每行头尾空白
            f.close()

            if (len(color_list)==9):
                for i in range(3):
                    for j in range(3):
                        #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                        canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill=str(color_list[i+j*3]),outline='black')
        else:
            for i in range(3):
                for j in range(3):
                    #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                    canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill='pink',outline='black')
    canvas.pack()#包装画布
    #魔方面位置
    canvas.place(x=draw_cube_x, y=draw_cube_y)
    print("(扫描运算)六面图发生一次变化")


result_lb_x , result_lb_y = 510,20 
def result_lb(window,print_str):
    import os
    from datetime import datetime
    result_lb = tk.Label(window,
                        text=print_str,justify='left',
                        width=88, height=10,
                        font=('Arial', 12),bg = '#ffffff',)
    result_lb.place(x = result_lb_x,y = result_lb_y)
    # 创建data文件夹（如果不存在）
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)
    
    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 构建完整文件路径
    file_path = os.path.join(data_folder, "PPC.log")
    
    try:
        # 追加模式打开文件
        with open(file_path, 'a', encoding='utf-8') as file:
            # 写入时间戳和内容，确保每行以时间戳开始
            file.write(f"\n[{current_time}] {print_str}\n")
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")


from tkinter import scrolledtext
import logging
def loging_text(root):
    # 创建带滚动条的文本框
    log_text = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, width=80, height=30, state=tk.DISABLED
    )
    log_text.pack(fill=tk.BOTH, expand=True)
    log_text.place(x = 940,y = 460)
    
    