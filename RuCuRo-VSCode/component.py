
import tkinter as tk
import os
def draw_cube_ja(window):
    colors = ['green', 'red', 'orange', 'white', 'yellow', 'blue']
    color_codes = ['g', 'r', 'o', 'w', 'y', 'b']
    
    # 创建第一个三面图 - 右侧、前面、上面
    canvas1 = tk.Canvas(window, width=720, height=480, bg="white")
    canvas1.place(relx=0.05, rely=0.5, anchor="w")
    
    # 定义第一组三个面的位置 (右侧、前面、上面)
    positions1 = {
        'green': (1, 1),   # 右侧
        'red': (0, 1),     # 前面
        'white': (1, 0)    # 上面
    }
    
    # 绘制第一组三个面
    for color in ['green', 'red', 'white']:
        col, row = positions1[color]
        x = 10 + col * 200
        y = 50 + row * 200
        
        color_code = color_codes[colors.index(color)]
        color_list = read_color_data(color_code)
        
        draw_face(canvas1, x, y, color_list, color)
    
    # 创建第二个三面图 - 左侧、后面、下面
    canvas2 = tk.Canvas(window, width=720, height=480, bg="white")
    canvas2.place(relx=0.95, rely=0.5, anchor="e")
    
    # 定义第二组三个面的位置 (左侧、后面、下面)
    positions2 = {
        'orange': (1, 1),  # 左侧
        'blue': (0, 1),    # 后面
        'yellow': (1, 0)   # 下面
    }
    
    # 绘制第二组三个面
    for color in ['orange', 'blue', 'yellow']:
        col, row = positions2[color]
        x = 10 + col * 200
        y = 50 + row * 200
        
        color_code = color_codes[colors.index(color)]
        color_list = read_color_data(color_code)
        
        draw_face(canvas2, x, y, color_list, color)

def read_color_data(color_code):
    """读取颜色数据文件"""
    try:
        if os.path.exists(f'data/{color_code}.txt'):
            with open(f'data/{color_code}.txt', 'r', encoding='utf-8') as f:
                color_list = [line.strip() for line in f.readlines()]
            if len(color_list) == 9:
                return color_list
    except Exception as e:
        print(f"Error reading {color_code}.txt: {e}")
    return [color_code_to_name(color_code)] * 9

def color_code_to_name(code):
    """将颜色代码转换为颜色名称"""
    color_map = {'g': 'green', 'r': 'red', 'o': 'orange', 
                 'w': 'white', 'y': 'yellow', 'b': 'blue'}
    return color_map.get(code, 'pink')

def draw_face(canvas, x, y, color_list, default_color):
    """绘制单个魔方面"""
    # 绘制面标题
    face_names = {'green': '右面', 'red': '前面', 'white': '上面',
                  'orange': '左面', 'blue': '后面', 'yellow': '下面'}
    canvas.create_text(x + 80, y - 10, text=face_names.get(default_color, default_color), 
                      font=('SimHei', 10), fill="black")
    
    # 绘制9个小方块
    for i in range(3):
        for j in range(3):
            x1 = x + 50 * i
            y1 = y + 50 * j
            x2 = x + 50 * (i + 1)
            y2 = y + 50 * (j + 1)
            
            # 获取填充颜色，如果没有数据则使用默认颜色
            fill_color = color_list[i + j * 3] if i + j * 3 < len(color_list) else default_color
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black", width=2)
            
            # 添加中心小圆点以增强视觉效果
            canvas.create_oval(x1 + 20, y1 + 20, x1 + 30, y1 + 30, fill="white", outline="")

def open():
    window = tk.Tk()
    window.title("湖州职业技术学院")
    window.geometry("1440x960")
    draw_cube_jb_btn = tk.Button(window,
        text='识别绘图',      
        width=12, height=2,
        font=('Arial', 12),bg = 'Yellow',
        command=draw_cube_ja(window)) 
    draw_cube_jb_btn.place(relx = 0.4,rely = 0.9) 
    window.mainloop()