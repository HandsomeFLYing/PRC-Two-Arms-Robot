import serial
import time



    #创建端口对象
try:
    #传入参数
    arduino_ser = serial.Serial('COM5', 115200)
except Exception as e:
    print('（s001）端口连接失败,错误原因：01)',e)

#arduino_ser = serial.Serial('COM5', 115200)



def ser_init():
    try:
        if arduino_ser.isOpen == False:
            arduino_ser.open()                # 打开串口
    except Exception as e:
        print('（s002）端口打开失败,错误原因：02)',e)

def ser_close():
    try:
        if arduino_ser != None:
            arduino_ser.close()
    except Exception as e:
        print('（s003）端口异常,错误原因：03)',e)

def ser_send(string):
    try:
        arduino_ser.write(string)
        return 1
    except Exception as e:
        print('（s004）端口上传异常,错误原因：04)',e)
        return 0


def ser_recv():
    try:
        while True:
            # 获得接收缓冲区字符
            count = arduino_ser.inWaiting()
            # 读取内容并显示
            if count == 0:
                break
            recv = arduino_ser.read(count)
            print(recv)
            # 清空接收缓冲区
            arduino_ser.flushInput()
            # 必要的软件延时
            time.sleep(0.1)
            return recv   
    except Exception as e:
        print('（s005）端口传输失败,错误原因：05)',e)

def show_help(messagebox):
        """显示帮助信息"""
        help_text = """
        魔方命令帮助
        
        1. 视图去旋转说明:
            u_mapping = 'ZRz' if loop_num >= 8 else 'xFX'
            u_prime_mapping = 'Zrz' if loop_num % 8 >= 4 else 'xfX'
            d_mapping = 'zRZ' if loop_num % 4 >= 2 else 'XFx'
            d_prime_mapping = 'zrZ' if loop_num % 2 else 'Xfx'
    
            'R': 'R', 'r': 'r',
            'L': 'ZZRZZ', 'l': 'ZZrZZ',
            'U': u_mapping, 'u': u_prime_mapping,
            'D': d_mapping, 'd': d_prime_mapping,
            'F': 'F', 'f': 'f',
            'B': 'XXFXX', 'b': 'XXfXX'
        
        2. 步骤旋转说明:
           'ob': ' ', 'ow': 'x', 'og': 'XX', 'oy': 'X',
            'rb': 'ZZ', 'rw': 'ZZx', 'rg': 'ZZXX', 'ry': 'xZZ',
            'yb': 'z', 'yo': 'xz', 'yg': 'XXz', 'yr': 'Xz',
            'wb': 'Z', 'wo': 'XZ', 'wg': 'XXZ', 'wr': 'xZ',
            'go': 'xzX', 'gy': 'zX', 'gr': 'xZx', 'gw': 'Zx',
            'br': 'xZX', 'bw': 'zx', 'bo': 'XZX', 'by': 'ZX'
        """
        messagebox.showinfo("帮助", help_text)
#def main():
#    while True:
#        # 获得接收缓冲区字符
#        count = ser.inWaiting()
#        if count != 0:
#            # 读取内容并显示
#            recv = ser.read(count)
#            print(recv)
#        # 清空接收缓冲区
#        ser.flushInput()
#        # 必要的软件延时
#        time.sleep(0.1)
#
#if __name__ == '__main__':
#    try:
#    # 打开串口
#        ser = serial.Serial('/dev/ttyAMA0', 115200)
#        if ser.isOpen == False:
#            ser.open()                # 打开串口
#        ser.write(b"rRZzXfxFRRXX")
#        #ser.write(b"rzrzRRzRzFZZrZZxfxFXXrZRzRzrZFFzRZRRFFxfxFFXXZZRRZrzRR")
#        main()
#    except KeyboardInterrupt:
#        if ser != None:
#            ser.close()

def connect_to_arduino(port='COM5', baudrate=115200, timeout=1, disconnect=False,result_lb = "null",window = ""):
    """连接或断开Arduino串口"""
    global arduino_ser  # 使用全局变量存储串口对象
    
    if disconnect:
        try:
            if arduino_ser and arduino_ser.is_open:
                arduino_ser.close()
                print(f"（连接）已断开 {port} 连接")
                if result_lb != "null" :
                    result_lb(window,f"(连接）已断开 {port} 连接")
                return True
            else:
                print(f"（s006）断开失败：端口 {port} 未连接")
                if result_lb != "null" :
                    result_lb(window,f"断开失败：端口 {port} 未连接")
                return False
        except Exception as e:
            print('（s006）异常的断开操作：',e)
            if result_lb != "null" :
                result_lb(window,f"断开失败：端口 {port} 未连接")
        
    else:
        # 保持原有连接逻辑...
        try:
            arduino_ser = serial.Serial(port, baudrate, timeout=timeout)
            if arduino_ser.is_open:
                if result_lb != "null" :
                    result_lb(window,f"（连接）成功连接到 {port}，波特率 {baudrate}")
                print(f"（连接）成功连接到 {port}，波特率 {baudrate}")
                return arduino_ser
        except Exception as e:
            print('（s001）端口连接失败,错误原因：02)',e)
            if result_lb != "null" :
                result_lb(window,f"连接失败：端口 {port} 不存在或不支持")