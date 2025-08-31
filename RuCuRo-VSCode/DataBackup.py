import datetime
import shutil
import os
from pathlib import Path

def Backuo():
        print("?文件系统")
        # 示例：将 'source_folder' 复制到当前目录下以当前时间命名的文件夹
        source_folder = "data"  # 替换为实际的源文件夹路径
        picture = "picture"
        log_fill = "log"
        if not os.path.exists(source_folder):
            print(f"（备份）错误：源文件夹 '{source_folder}' 不存在")
        if not os.path.exists(picture):
            print(f"（备份）错误：源文件夹 '{picture}' 不存在")
        # 如果没有指定目标位置，使用当前时间创建文件夹
        if None is None:
            time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            data_time = "backup/" + time
            picture_time = "test/" + time
            parent_dir = os.getcwd()  # 当前工作目录
            target_dir_data = os.path.join(parent_dir, data_time)
            target_dir_picture = os.path.join(parent_dir, picture_time)
        
        # 复制文件夹
        try:
            folder_path = Path('data')
            data_su = len(list(folder_path.glob('*')))
            if data_su > 1:    
                shutil.copytree(source_folder, target_dir_data)
                print(f"（备份）成功复制文件夹到: {target_dir_data}")
            else:
                print("（备份）无文件备份")
            
        except FileExistsError:
            print(f"（备份）错误：目标文件夹 '{target_dir_data}' 已存在")
        except Exception as e:
            print(f"（备份）错误：复制过程中出现问题: {e}")

        try:
            folder_path = Path('picture')
            picture_su = len(list(folder_path.glob('*')))
            if picture_su:
                shutil.copytree(picture, target_dir_picture)
                print(f"（备份）成功复制文件夹到: {target_dir_picture}")
            else:
                print("（备份）无文件备份")
        except FileExistsError:
            print(f"（备份）错误：目标文件夹 '{target_dir_picture}' 已存在")
        except Exception as e:
            print(f"（备份）错误：复制过程中出现问题: {e}")


#def remove_color():
#   color = ['white','red','green','yellow','orange','blue']
#    for i in range(6):
#        if os.path.exists('data/sort.txt'):
 #          os.remove('data/sort.txt')
 #       if os.path.exists('data/'+color[i]+'.txt'):
 #          os.remove('data/'+color[i]+'.txt')
 #   print("异常的无结？")


