'''Author y1shin@163.com'''
import os
import sys
import argparse
import platform
import matplotlib.pyplot as plt

logo = '''
          __         _       _         
         /_ |       | |     (_)        
  _   _   | |  ___  | |__    _   _ __  
 | | | |  | | / __| | '_ \  | | | '_ \ 
 | |_| |  | | \__ \ | | | | | | | | | |
  \__, |  |_| |___/ |_| |_| |_| |_| |_|
   __/ |                               
  |___/                                 
'''

class END:
    def Without_Match():
        print("[-] 解密失败,请联系QQ:2729913542更新USB数据")
    def Message():
        print("[+] 工具由y1shin开发,欢迎加QQ:2729913542与我讨论")

class GET_START:
    def Get_Basic_Parameter():
        parser = argparse.ArgumentParser()
        parser.add_argument('-f' ,type=str ,default=None ,required=True ,
                            help='输入文件路径')
        parser.add_argument('-p' ,type=str ,default=None ,required=True ,
                            help='输入需要提取的srcIP')
        parser.add_argument('-d' ,type=str ,default=None ,required=True ,
                            help='输入需要提取的字段名:usbhid.data/usb.capdata')
        args = parser.parse_args()
        return args.f ,args.p ,args.d
        
    def Build_Cmd_Get_Data(file_name:str ,des_IP:str ,field_name:str):
        os.system(f"tshark -r {file_name} -T fields -Y 'usb.src=={des_IP}' -e {field_name} > temp_data.out" )
        os.system(f"tshark -r {file_name} -T fields -Y \"usb && usb.src!=host && usb.src!={des_IP}\" -e \"usb.idProduct\" > temp_id.out""")
        os.system(f"tshark -r {file_name} -T fields -Y \"usb && usb.src!=host && usb.src!={des_IP}\" -e \"usb.idVendor\" > temp_vendor.out""")
        
        f = open("temp_data.out")
        USB_Value_List = f.readlines()
        f.close()

        f = open("temp_id.out")
        USB_Device_Id = f.read().strip().split()
        f.close()

        f = open("temp_vendor.out")
        USB_Vendor_Id = f.read().strip().split()
        os.system(f"rm temp_data.out | rm temp_id.out | rm temp_vendor.out")

        ID = {}
        for i in range(len(USB_Vendor_Id)):
            ID[USB_Vendor_Id[i]] = USB_Device_Id[i]
        
        return USB_Value_List ,ID

class KEYBOARD:
    '''
    Leftover Capture Data(usb.capdata): 0200040000000000
    [0:2]->binary:00000010(按下了Left Shift) :
        数据由大端储存
    {   按下了什么功能键,对应的值为1,则已按下
        bit_0:Left Ctrl
        bit_1:Left Shift
        bit_2:Left Alt
        bit_3:Left Win
        bit_4:Right Ctrl
        bit_5:Right Shift
        bit_6:Right Alt
        bit_7:Right Win
    }
    [4:6]:按下的键盘上的键,如果短时间按了两个键,那么[6:8]也会有数据
    '''
    # 还原键盘的按键情况
    def Value_2_PlainText(data_list):
        normal_Keys = {
        "04":"a", "05":"b", "06":"c", "07":"d", "08":"e","09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j","0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o","13":"p", "14":"q", "15":"r", "16":"s", "17":"t","18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y","1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4","22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"\n","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":" ","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>","46":"<PRTSC>","47":"<SCR>","48":"<PAUSE>","49":"<INSERT>","4a":"<HOME>","4b":"<PGUP>","4c":"<DEL FORWARD>","4d":"<END>","4e":"<PGDW>","4f":"<RIGHTARROW>","50":"<LEFTARROW>","51":"<DOWNARROW>","52":"<UPARRWO>","00":"","":""}
        shift_Keys = {
        "04":"A", "05":"B", "06":"C", "07":"D", "08":"E", "09":"F", "0a":"G", "0b":"H", "0c":"I", "0d":"J", "0e":"K", "0f":"L", "10":"M", "11":"N", "12":"O", "13":"P", "14":"Q", "15":"R", "16":"S", "17":"T","18":"U", "19":"V", "1a":"W", "1b":"X", "1c":"Y","1d":"Z","1e":"!", "1f":"@", "20":"#", "21":"$","22":"%", "23":"^","24":"&","25":"*","26":"(","27":")","28":"\n","29":"<ESC>","2a":"<DEL>","2b":"\t","2c":" ","2d":"_","2e":"+","2f":"{","30":"}","31":"|","32":"<NON>","33":"\"","34":":","35":"<GA>","36":"<","37":">","38":"?","39":"<CAP>","3a":"<F1>","3b":"<F2>","3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>","46":"<PRTSC>","47":"<SCR>","48":"<PAUSE>","49":"<INSERT>","4a":"<HOME>","4b":"<PGUP>","4c":"<DEL FORWARD>","4d":"<END>","4e":"<PGDW>","4f":"<RIGHTARROW>","50":"<LEFTARROW>","51":"<DOWNARROW>","52":"<UPARRWO>","00":""}
        CAP_Count = 0 # 默认开始是小写
        result = ""

        for i in data_list:
            i = i.strip("\n")
            single_press = i[4:6]
            Function_press_bit = str(bin(int(i[0:2]))[2:].zfill(8)[::-1])
            
            # 计算功能键的按下情况
            Function_press_dir = {"[Ctrl]":0 ,"[Shift]":0 ,"[Alt]":0 ,"[Win]":0}
            if Function_press_bit[0] != "0" or Function_press_bit[4] != "0":
                Function_press_dir["[Ctrl]"] = 1
            if Function_press_bit[1] != "0" or Function_press_bit[5] != "0":
                Function_press_dir["[Shift]"] = 1
            if Function_press_bit[2] != "0" or Function_press_bit[6] != "0":
                Function_press_dir["[Alt]"] = 1
            if Function_press_bit[3] != "0" or Function_press_bit[7] != "0":
                Function_press_dir["[Win]"] = 1

            # 判断是否为有效press
            if single_press not in normal_Keys or single_press not in shift_Keys:
                continue

            # 排除重复press
            if i[4:6] != "00" and i[6:8] != "00":
                continue

            # 判断按下大写键没
            if single_press == "39":
                CAP_Count += 1
                continue

            # 输出功能键组合
            if 1 in Function_press_dir.values() and (Function_press_dir["[Alt]"] == 1 or Function_press_dir["[Ctrl]"] == 1 or Function_press_dir["[Win]"] == 1):
                for Func_tuple in Function_press_dir.items():
                    if Func_tuple[1] == 1:
                        print(f"{Func_tuple[0]} {shift_Keys[single_press]}")

            # 输出按下的键位
            CAP_Judge = (CAP_Count + Function_press_dir["[Shift]"])%2
            if CAP_Judge == 0:
                print(normal_Keys[single_press] ,end="")
            elif CAP_Judge == 1:
                print(shift_Keys[single_press] ,end="")

class MOUSE:
    '''
    Leftover Capture Data(usb.capdata): 0205fa00
    [0:2]->binary:00000010(正在按鼠标右键){
    大端储存,数据==1则按下,
        bit_0:鼠标左键
        bit_1:鼠标右键
        bit_2:鼠标中键
        bit_[3:7]:保留位
    }
    '''
    # 将鼠标轨迹画出来
    def Value_2_plt(data_list):
        x_dir ,y_dir = [] ,[]
        x_pos ,y_pos = 0 ,0
        x_list ,y_list = [] ,[]

        for i in data_list:
            i = i.strip("\n")
            x_offset = int(i[2:4] ,16)
            y_offset = int(i[4:6] ,16)
            if x_offset > 127:
                x_offset -= 256
            if y_offset > 127:
                y_offset -= 256
            x_pos += x_offset
            y_pos += y_offset
            
            x_dir.append((x_pos ,i[0:2]))
            y_dir.append((-y_pos ,i[0:2]))
        
        clear_option = str(input("需要清除多余的数据吗?[Y/N]:")).upper()
        press_option = str(input("需要输出鼠标按键二进制码吗?[y/N](slow):")).upper()
        if press_option == "Y" or press_option == "\n":
            MOUSE.Get_Mouse_press(data_list)
        # 清理多余数据，如果数据头是一样的，则忽略
        if clear_option == "Y" or clear_option == "\n":
            cleared_x_list ,cleared_y_list = [] ,[]
            for i in x_dir:
                if i[1] != "00":
                    cleared_x_list.append(i[0])
                elif i[1] == "00":
                    continue
            for i in y_dir:
                if i[1] != "00":
                    cleared_y_list.append(i[0])
                elif i[1] == "00":
                    continue
            # 输出结果
            plt.title("NORMAL_MOUSE")
            plt.scatter(x=cleared_x_list ,y=cleared_y_list)
            plt.show()
        else:
            x_list ,y_list = [] ,[]
            for i in x_dir:
                x_list.append(i[0])
            for i in y_dir:
                y_list.append(i[0])
            plt.title("NORMAL_MOUSE")
            plt.scatter(x=x_list ,y=y_list)
            plt.show()
    # 获取鼠标三个按键的二进制，这一段写的很臭，用处估计也不大
    def Get_Mouse_press(data_list):
        Mouse_left_press = ""
        Mouse_right_press = ""
        Mouse_mid_press = ""
        for i in data_list:
            i = i.strip("\n")
            data = str(bin(int(i ,16))[2:].zfill(8))[::-1]
            if data[0] == "1":
                Mouse_left_press += "1"
            else:
                Mouse_left_press += "0"
            if data[1] == "1":
                Mouse_right_press += "1"
            else:
                Mouse_right_press += "0"
            if data[2] == "1":
                Mouse_mid_press += "1"
            else:
                Mouse_mid_press += "0"
        # 左键数据
        if "1" not in Mouse_left_press:
            print(f"[-] Mouse_left_press: NOTHING")
        else:
            f = open("./Mouse_LEFTKEY.out" ,"w")
            f.write(Mouse_left_press)
            f.close()
            print(f"[+] 左键数据已经保存在了运行目录下")
        # 右键数据
        if "1" not in Mouse_right_press:
            print(f"[-] Mouse_right_press: NOTHING")
        else:
            f = open("./Mouse_RIGHTKEY.out" ,"w")
            f.write(Mouse_right_press)
            f.close()
            print(f"[+] 右键数据已经保存在了运行目录下")
        # 中键数据
        if "1" not in Mouse_mid_press:
            print(f"[-] Mouse_mid_press: NOTHING")
        else:
            f = open("./Mouse_MIDKEY.out" ,"w")
            f.write(Mouse_mid_press)
            f.close()
            print(f"[+] 中键数据已经保存在了运行目录下")

class WACOM:
    # Wacom Co., Ltd(0x056a)
    def CTL_480(data_list):
        '''
        型号:CTL-480 [Intuos Pen (S)] (0x030e)
        HID Data(usbhid.data): 02f1560e790fe9022800
        [0:4]==02f1是有效数据  x坐标[4:8]  y坐标[8:12]  
        坐标储存是小端储存
        '''
        print("[+] 型号:Wacom CTL-480 [Intuos Pen (S)] (0x030e)\n")
        x_list ,y_list = [],[]
        for i in data_list:
            i = i.strip("\n")
            if i[0:4] == "02f1":
                x_pos = int(i[4:6] ,16) + int(i[6:8] ,16)*256
                y_pos = int(i[8:10] ,16) + int(i[10:12] ,16)*256
                x_list.append(x_pos)
                y_list.append(-y_pos)
        plt.scatter(x=x_list ,y=y_list)
        plt.title("CTL 480")
        plt.show()

    def PTH_660(data_list):
        '''
        型号:PTH-660 [Intuos Pro (M)] (0x0357)
        HID Data(usbhid.data): 10614157000a1f00bd191404000000000084308094420810004208
        [16:18]!=00即为有效数据  x坐标[4:8]  y坐标[10:14]
        坐标储存是小端储存
        '''
        print("[+] Wacom 型号:PTH-660 [Intuos Pro (M)] (0x0357)\n")
        x_list ,y_list = [],[]
        for i in data_list:
            i = i.strip("\n")
            if len(i) != 54:
                continue
            if i[16:18] != "00" :
                x_pos = int(i[4:6] ,16) + int(i[6:8] ,16)*256
                y_pos = int(i[10:12] ,16) + int(i[12:14] ,16)*256
                x_list.append(x_pos)
                y_list.append(-y_pos)
        plt.scatter(x=x_list ,y=y_list)
        plt.title("PTH 660")
        plt.show()

class LOG:
    # Logitech, Inc.(0x046d)
    def LOG_Lightspeed_Reveiver(data_list):
        '''
        型号:Lightspeed Receiver(0xc539)
        usbhid.data = 020000130000000000
        去掉头部两个标识符就是正常的鼠标流量
        '''
        print("[+] 型号:Logitech Lightspeed Receiver(0xc539)\n")
        changed_datalist = []
        for i in data_list:
            i = f"{i[2:4]}{i[6:8]}{i[10:12]}00"
            changed_datalist.append(i)
        MOUSE.Value_2_plt(changed_datalist)
    
    def LOG_G502_MOUSE(data_list):
        '''
        型号:G502 SE HERO Gaming Mouse(0xc08b)
        HID Data(usbhid.data):0000feff02000000
        [4:6]:x坐标  [8:10]:y坐标
        '''
        print("[+] 型号:Logitech G502 SE HERO Gaming Mouse(0xc08b)\n")
        changed_data = []
        for i in data_list:
            # 将这个数据转化成基础的鼠标流量的数据结构
            i = f"{i[0:2]}{i[4:6]}{i[8:10]}00"
            changed_data.append(i)
        MOUSE.Value_2_plt(changed_data)

    def Mouse(data_list):
        '''
        型号:Mouse(0xc077)
        数据类型:普通类型
        '''
        print("[+] 型号:Logitech Mouse(0xc077)\n")
        MOUSE.Value_2_plt(data_list)

    def Unknown_keyboard(data_list):
        '''
        型号:Unknown(0xc341)
        数据类型:普通类型
        '''
        print("[+] 型号:Logitech Unknow Keyboard Type(0xc341)\n")
        KEYBOARD.Value_2_PlainText(data_list)

    def G304_Wireless(data_list):
        '''
        型号: G304 无线鼠标(0xc53f)
        数据结构(usbhid.data):020100ffff01000000
        [2:4] press    [6:8] x位移  [10:12] y位移
        '''
        print("[+] G304 Wireless(0xc53f)")
        changed_list = []
        for i in data_list:
            i = f"{i[2:4]}{i[6:8]}{i[10:12]}00"
            changed_list.append(i)
        MOUSE.Value_2_plt(changed_list)

    def G102_Wire(data_list):
        '''
        型号: G102 有线鼠标
        '''
        ...

class Razer:
    # Razer USA, Ltd (0x1532)

    def Basilisk_Mouse(data_list):
        '''
        型号:RC30-0315, Gaming Mouse [Basilisk x HyperSpeed] (0x0083)
        数据结构(usbhid.data):01feff00feffffff
        [0:2] press  [2:4] x位移 [4:6] y轴
        '''
        print("[+] RC30-0315, Gaming Mouse [Basilisk x HyperSpeed] (0x0083)")
        changed_list = []
        for i in data_list:
            i = f"{i[0:2]}{i[2:4]}{i[4:6]}00"
            changed_list.append(i)
        MOUSE.Value_2_plt(changed_list)

class Apple:
    # Apple, Inc.(0x05ac)
    def ANSI(data_list):
        '''
        型号:Aluminium Keyboard (ANSI) (0x024f)
        暂且当成普通的键盘来解
        '''
        print("[+] 型号:Apple Aluminium Keyboard (ANSI)(0x024f)\n")
        normal_Keys = {
        "04":"a", "05":"b", "06":"c", "07":"d", "08":"e","09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j","0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o","13":"p", "14":"q", "15":"r", "16":"s", "17":"t","18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y","1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4","22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"\n","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":" ","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>","46":"<PRTSC>","47":"<SCR>","48":"<PAUSE>","49":"<INSERT>","4a":"<HOME>","4b":"<PGUP>","4c":"<DEL FORWARD>","4d":"<END>","4e":"<PGDW>","4f":"<RIGHTARROW>","50":"<LEFTARROW>","51":"<DOWNARROW>","52":"<UPARRWO>","00":"","":""}
        for i in data_list:
            i = i.strip("\n")
            print(normal_Keys[i[4:6]] ,end="")

if __name__ == "__main__":
    Judge_Counter = 0
    if platform.system() != 'Linux':
        print(f"您当前的操作系统{platform.system()},本工具只适用于Linux系统!")
        exit(-1)
    file ,ip ,field = GET_START.Get_Basic_Parameter()
    Field_Value ,ID = GET_START.Build_Cmd_Get_Data(file_name=file ,des_IP=ip ,field_name=field)
    print(f"[+] [DEVICE_LIST] {ID}\n[+] 您可以在USB_ID_List.txt中查找具体的设备名称\n" ,"-"*50)
    if "0x046d" in ID:
        Judge_Counter += 1
        # 罗技的设备
        if ID["0x046d"] == "0xc539":
            LOG.LOG_Lightspeed_Reveiver(Field_Value)
        elif ID["0x046d"] == "0xc08b":
            LOG.LOG_G502_MOUSE(Field_Value)
        elif ID["0x046d"] == "0xc077":
            LOG.Mouse(Field_Value)
        elif ID["0x046d"] == "0xc341":
            LOG.Unknown_keyboard(Field_Value)
        elif ID["0x046d"] == "0xc53f":
            LOG.G304_Wireless(Field_Value)
        elif ID["0x046d"] == "...":
            LOG.G102_Wire(Field_Value)
        print("\n"*3 ,"-"*50)

    if "0x056a" in ID:
        Judge_Counter += 1
        # Wacom 数位板
        if ID["0x056a"] == "0x030e":
            WACOM.CTL_480(Field_Value)
        elif ID["0x056a"] == "0x0357":
            WACOM.PTH_660(Field_Value)
        print("\n"*3 ,"-"*50)

    if "0x05ac" in ID:
        Judge_Counter += 1
        # 苹果的设备 但是没有钱买苹果( 所以这个ID就只能搁置一下
        # 等待完善ing...
        if ID["0x05ac"] == "0x024f":
            Apple.ANSI(Field_Value)
        print("\n"*3 ,"-"*50)

    if "0x1532" in ID:
        Judge_Counter += 1
        # 雷蛇的设备
        if ID["0x1532"] == "0x0083":
            Razer.Basilisk_Mouse(Field_Value)
        print("\n"*3 ,"-"*50)

    if Judge_Counter == 0:
        if len(Field_Value[1].strip("\n")) == 16:
            KEYBOARD.Value_2_PlainText(Field_Value)
        elif len(Field_Value[1].strip("\n")) == 8:
            MOUSE.Value_2_plt(Field_Value)
        else:
            END.Without_Match()
        print("\n"*3 ,"-"*50)

    END.Message()
