import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FolderTxtViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PRC日志查看器")
        self.root.geometry("1280x800")  # 增加宽度以容纳状态显示框
        
        # 创建样式
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('SimHei', 10))
        self.style.configure('TButton', font=('SimHei', 10))
        self.style.configure('TLabelframe.Label', font=('SimHei', 10))
        
        # 颜色定义
        self.color = ['green', 'red', 'orange', 'white', 'yellow', 'blue']
        self.color_ = ['g', 'r', 'o', 'w', 'y', 'b']
        
        # 初始化变量
        self.current_dir = tk.StringVar()
        self.selected_folder_path = tk.StringVar()
        self.canvas = None
        
        # 创建顶部区域 - 分为魔方显示和状态显示
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 左侧：魔方显示区域
        left_top_frame = ttk.LabelFrame(top_frame, text="魔方六面状态", padding=10)
        left_top_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建魔方画布
        self.canvas = tk.Canvas(left_top_frame, width=180, height=360, bg="#FA9FFF")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 右侧：状态显示框
        right_top_frame = ttk.LabelFrame(top_frame, text="日志状态信息", padding=10)
        right_top_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # 创建状态显示文本框
        self.status_display = tk.Text(right_top_frame, height=15, width=40, font=('SimHei', 10), wrap=tk.WORD)
        self.status_display.pack(fill=tk.BOTH, expand=True)
        self.status_display.config(state=tk.DISABLED)  # 设置为只读
        
        # 顶部：选择文件夹按钮和当前路径显示
        path_frame = ttk.Frame(self.root, padding=10)
        path_frame.pack(fill=tk.X)
        
        ttk.Button(path_frame, text="选择根目录", command=self.select_root_directory).pack(side=tk.LEFT)
        ttk.Label(path_frame, text="根目录:", style='TLabel').pack(side=tk.LEFT, padx=5)
        ttk.Label(path_frame, textvariable=self.current_dir, style='TLabel', wraplength=500).pack(side=tk.LEFT)
        
        ttk.Label(path_frame, text="当前文件夹:", style='TLabel').pack(side=tk.LEFT, padx=10)
        ttk.Label(path_frame, textvariable=self.selected_folder_path, style='TLabel', wraplength=300).pack(side=tk.LEFT)
        
        # 中间区域：分为左右两部分（列表区和内容区）
        mid_frame = ttk.Frame(self.root, padding=10)
        mid_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：文件夹列表区
        list_frame = ttk.LabelFrame(mid_frame, text="日志文件列表", padding=5)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建文件夹列表
        self.folder_listbox = tk.Listbox(list_frame, font=('SimHei', 10), selectmode=tk.SINGLE, 
                                        yscrollcommand=scrollbar.set)
        self.folder_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.folder_listbox.yview)
        
        # 绑定双击事件
        self.folder_listbox.bind('<Double-1>', self.on_folder_double_click)
        
        # 右侧：文本内容区
        content_frame = ttk.LabelFrame(mid_frame, text="日志文件内容", padding=5)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 创建多行文本框
        self.text_area = tk.Text(content_frame, font=('SimHei', 10), wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # 创建水平滚动条
        h_scrollbar = ttk.Scrollbar(self.text_area, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.config(xscrollcommand=h_scrollbar.set)
        h_scrollbar.config(command=self.text_area.xview)
        
        # 初始化时尝试打开backup文件夹
        self.try_open_backup_folder()
        
        # 绘制魔方
        self.draw_cube()
    
    def try_open_backup_folder(self):
        """尝试打开同目录下的backup文件夹作为根目录"""
        current_path = os.path.abspath(os.path.dirname(__file__))
        backup_path = os.path.join(current_path, "backup")
        
        if os.path.exists(backup_path) and os.path.isdir(backup_path):
            self.current_dir.set(backup_path)
            self.selected_folder_path.set(backup_path)
            self.update_status_display(f"已默认打开备份文件夹: {backup_path}")
            self.load_folders(backup_path)
            self.text_area.insert(tk.END, f"已默认打开备份文件夹: {backup_path}\n")
        else:
            self.current_dir.set(current_path)
            self.selected_folder_path.set(current_path)
            self.update_status_display(f"未找到backup文件夹，默认打开当前目录: {current_path}")
            self.load_folders(current_path)
            self.text_area.insert(tk.END, f"未找到backup文件夹，默认打开当前目录: {current_path}\n")
            messagebox.showinfo("提示", f"未找到backup文件夹，已打开当前目录\n\n如需使用默认功能，请在程序同目录下创建backup文件夹")
    
    def select_root_directory(self):
        """选择根目录并显示其中的文件夹"""
        directory = filedialog.askdirectory()
        if directory:
            self.current_dir.set(directory)
            self.selected_folder_path.set(directory)
            self.update_status_display(f"已选择根目录: {directory}")
            self.load_folders(directory)
            self.update_cube()  # 更新魔方显示
    
    def load_folders(self, directory):
        """加载并显示指定目录下的所有文件夹"""
        self.folder_listbox.delete(0, tk.END)
        try:
            folders = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    folders.append(item)
            
            # 按名称降序排列文件夹
            folders.sort(reverse=True)
            
            for folder in folders:
                self.folder_listbox.insert(tk.END, folder)
                
        except Exception as e:
            messagebox.showerror("错误", f"无法加载文件夹: {str(e)}")
    
    def on_folder_double_click(self, event):
        """双击文件夹时读取其中的txt文件并更新魔方"""
        selection = self.folder_listbox.curselection()
        if not selection:
            return
            
        folder_name = self.folder_listbox.get(selection[0])
        folder_path = os.path.join(self.current_dir.get(), folder_name)
        self.selected_folder_path.set(folder_path)
        self.update_status_display(f"已选择文件夹: {folder_path}")
        
        # 读取txt文件内容
        self.read_txt_files(folder_path)
        self.update_cube()  # 更新魔方显示
        self.read_ppc_file(folder_path)  # 读取PPC.txt文件内容
    
    def read_txt_files(self, folder_path):
        """读取指定文件夹中的所有txt文件内容"""
        self.text_area.delete(1.0, tk.END)  # 清空文本区
        
        try:
            txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
            
            if not txt_files:
                self.text_area.insert(tk.END, "该文件中没有没有日志信息。")
                self.update_status_display("该日志文件中没有记录")
                return
                
            self.update_status_display(f"正在读取文件夹: {folder_path} 中的 {len(txt_files)} 个数据文件")
            
            for txt_file in txt_files:
                file_path = os.path.join(folder_path, txt_file)
                
                # 添加文件标题
                self.text_area.insert(tk.END, f"=== {txt_file} ===\n\n")
                
                try:
                    # 尝试使用utf-8编码读取
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    # 如果utf-8失败，尝试使用gbk编码
                    try:
                        with open(file_path, 'r', encoding='gbk') as f:
                            content = f.read()
                    except Exception as e:
                        content = f"无法读取文件: {str(e)}"
                
                # 添加文件内容
                self.text_area.insert(tk.END, content + "\n\n")
                
                # 添加分隔线
                self.text_area.insert(tk.END, "-" * 80 + "\n\n")
                
            # 滚动到顶部
            self.text_area.see(1.0)
            
            self.update_status_display(f"已成功读取 {len(txt_files)} 个数据文件")
            
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时出错: {str(e)}")
            self.update_status_display(f"读取文件时出错: {str(e)}")
    
    def update_cube(self):
        """更新魔方显示（仅重绘画布内容）"""
        self.draw_cube()
    
    def draw_cube(self):
        """绘制魔方，从选中的文件夹中读取文件"""
        # 清除旧画布内容
        self.canvas.delete("all")
        
        folder_path = self.selected_folder_path.get()
        if not folder_path:
            folder_path = self.current_dir.get()  # 若未选中文件夹，使用根目录
        
        self.update_status_display(f"正在从 {folder_path} 读取魔方数据...")
        
        for n in range(len(self.color)):
            col = row = 0
            if self.color[n] == 'white':
                col = 1
                row = 0
            elif self.color[n] == 'orange':
                col = 0
                row = 1
            elif self.color[n] == 'green':
                col = 1
                row = 1
            elif self.color[n] == 'red':
                col = 2
                row = 1
            elif self.color[n] == 'blue':
                col = 3
                row = 1
            elif self.color[n] == 'yellow':
                col = 1
                row = 2
            
            x = 10 + col * 120
            y = 10 + row * 120
            
            file_path = os.path.join(folder_path, self.color_[n] + '.txt')
            color_list = []
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        color_list = [line.strip() for line in f.readlines() if line.strip()]
                except Exception as e:
                    messagebox.showerror("错误", f"读取{file_path}时出错: {str(e)}")
                    color_list = []
            else:
                color_list = []
            
            if len(color_list) == 9:
                for i in range(3):
                    for j in range(3):
                        # 绘制矩形，填充颜色来自文件，边框为黑色
                        self.canvas.create_rectangle(
                            x + 35 * i, y + 35 * j,
                            x + 35 * (i + 1), y + 35 * (j + 1),
                            fill=color_list[i + j * 3], outline='black'
                        )
            else:
                for i in range(3):
                    for j in range(3):
                        # 绘制粉色方块作为默认
                        self.canvas.create_rectangle(
                            x + 35 * i, y + 35 * j,
                            x + 35 * (i + 1), y + 35 * (j + 1),
                            fill='pink', outline='black'
                        )
        
        self.update_status_display(f"已从{folder_path}读取文件并更新魔方状态")
        #print(f"已从{folder_path}读取文件并更新魔方状态")
    
    def update_status_display(self, message):
        """更新状态显示框内容"""
        self.status_display.config(state=tk.NORMAL)
        self.status_display.delete(1.0, tk.END)
        self.status_display.insert(tk.END, message)
        self.status_display.config(state=tk.DISABLED)
    
    def set_custom_status(self, message):
        """自定义状态显示框内容的公共接口"""
        self.update_status_display(message)
    
    def read_ppc_file(self, folder_path):
        """读取PPC.txt文件内容并更新状态显示"""
        ppc_file = os.path.join(folder_path, "PPC.log")
        
        if os.path.exists(ppc_file) and os.path.isfile(ppc_file):
            try:
                with open(ppc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.update_status_display(f"处理日志内容:\n\n{content}")
            except UnicodeDecodeError:
                try:
                    with open(ppc_file, 'r', encoding='gbk') as f:
                        content = f.read()
                        self.update_status_display(f"PPC.txt 内容:\n\n{content}")
                except Exception as e:
                    self.update_status_display(f"无法读取PPC.txt文件: {str(e)}")
            except Exception as e:
                self.update_status_display(f"无法读取PPC.txt文件: {str(e)}")
        else:
            self.update_status_display("版本过低日志或者无结果，可抛弃已无参考价值")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderTxtViewer(root)
    root.mainloop()