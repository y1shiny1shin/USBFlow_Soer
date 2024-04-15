'''Author y1shin@163.com'''
import os
import sys
import yaml
import argparse
import platform
import matplotlib.pyplot as plt
import operator

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
        print("-"*50 ,"\n[-] 解密失败,请联系QQ:2729913542更新USB数据")
    def Message():
        print("-"*50 ,"\n[+] 工具由y1shin开发,欢迎加QQ:2729913542与我讨论")

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
        
    def Build_Cmd_And_Get_Data(file_name:str ,des_IP:str ,field_name:str):
        Reponse_IP = des_IP[:-1]+"0"
        os.system(f'tshark -r {file_name} -T fields -Y "usb.src=={des_IP}" -e {field_name} > temp_data.out')
        os.system(f'tshark -r {file_name} -T fields -Y \"usb && usb.src!=host && usb.src!={des_IP}\" -e \"usb.idProduct\" > temp_id.out')
        os.system(f'tshark -r {file_name} -T fields -Y \"usb && usb.src!=host && usb.src!={des_IP}\" -e \"usb.idVendor\" > temp_vendor.out')
        os.system(f'tshark -r {file_name} -T fields -Y \"usb && usb.src!=host && usb.src=={Reponse_IP}\" -e \"usb.idVendor\" > temp_Response.out')
        os.system(f'tshark -r {file_name} -T fields -Y \"usb && usb.src!=host && usb.src=={Reponse_IP}\" -e \"usb.idProduct\" > temp_Res.out')
        
        with open("temp_data.out") as f:
            USB_Value_List = f.readlines()
        with open("temp_id.out") as f:
            USB_Device_Id = f.read().strip().split()
        with open("temp_vendor.out") as f:
            USB_Vendor_Id = f.read().strip().split()
        with open("temp_Response.out") as f:
            Des_VendorID = f.read().strip().split()
        with open("temp_Res.out") as f:
            Des_ProductID = f.read().strip().split()

        # 在zeror师傅的指导下，旨在增强代码的健壮性
        temp_dirlist = ["temp_data.out" ,"temp_id.out" ,"temp_vendor.out" ,"temp_Response.out" ,"temp_Res.out" ,] 
        for i in temp_dirlist:
            try:
                os.remove(i)
            except:
                print(f"运行名录下临时文件{i}未能删除,请手动删除")
        
        # 读取所有的ID值
        ID = []
        for i in range(len(USB_Vendor_Id)):
            ID.append((USB_Vendor_Id[i] ,USB_Device_Id[i]))
        
        # 这里是为了解决出题人只截取部分流量包的问题
        if len(Des_VendorID) != 0:
            return USB_Value_List ,ID ,(Des_VendorID[0] ,Des_ProductID[0])
        else:
            return USB_Value_List ,ID ,(None ,None)

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

        Func_Choice = input('需要输出所有的功能键吗?[y/n]:').upper()

        for i in data_list:
            i = i.strip("\n")
            single_press = i[4:6]
            Function_press_bit = str(bin(int(i[0:2] ,16))[2:].zfill(8)[::-1])

            Function_press_dir = {"[Ctrl]":0 ,"[Shift]":0 ,"[Alt]":0 ,"[Win]":0}
            # 计算功能键的按下情况
            if Function_press_bit[0] != "0" or Function_press_bit[4] != "0":
                Function_press_dir["[Ctrl]"] = 1
            if Function_press_bit[1] != "0" or Function_press_bit[5] != "0":
                Function_press_dir["[Shift]"] = 1
            if Function_press_bit[2] != "0" or Function_press_bit[6] != "0":
                Function_press_dir["[Alt]"] = 1
            if Function_press_bit[3] != "0" or Function_press_bit[7] != "0":
                Function_press_dir["[Win]"] = 1

            # 判断是否为有效press
            if (single_press not in normal_Keys) or (single_press not in shift_Keys):
                continue

            # 排除重复press
            if i[4:6] != "00" and i[6:8] != "00":
                continue

            # 判断按下大写键没
            if single_press == "39":
                CAP_Count += 1
                continue

            # 输出功能键组合
            if Func_Choice == "Y":
                if 1 in Function_press_dir.values() and (Function_press_dir["[Alt]"] == 1 or Function_press_dir["[Ctrl]"] == 1 or Function_press_dir["[Win]"] == 1):
                    for Func_tuple in Function_press_dir.items():
                        if Func_tuple[1] == 1:
                            print(f"{Func_tuple[0]} {shift_Keys[single_press]}")
            
            # 输出按下的键位
            CAP_Judge = (CAP_Count + Function_press_dir["[Shift]"])%2
            
            if Function_press_dir["[Shift]"] == 0:
                if CAP_Judge == 0:
                    print(normal_Keys[single_press].lower() ,end="")
                elif CAP_Judge == 1:
                    print(normal_Keys[single_press].upper() ,end="")
            else:
                if CAP_Judge == 0:
                    print(shift_Keys[single_press].lower() ,end="")
                elif CAP_Judge == 1:
                    print(shift_Keys[single_press].upper() ,end="")

        print("\n" ,"-"*50)

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
        # 本来是想用一个文件来存数据的，但是临时文件太多了，就用变量来存了，运行速度也大差不差
        Left_x_dir ,Left_y_dir = [] ,[]
        Right_x_dir ,Right_y_dir = [] ,[]
        Mid_x_dir ,Mid_y_dir = [] ,[]
        All_x_dir ,All_y_dir = [] ,[]
        pos_x ,pos_y = 0 ,0
        offset_x ,offset_y = 0 ,0
        for i in data_list:
            press_state = bin(int(i[0:2] ,16))[2:].zfill(8)[::-1]
            offset_x = int(i[2:4] ,16)
            offset_y = int(i[4:6] ,16)
            if offset_x > 127:
                offset_x -= 256
            if offset_y > 127:
                offset_y -= 256
            pos_x += offset_x
            pos_y += offset_y
            
            # 这段是用来记录所有的按键情况的痕迹
            if press_state[0] == "1":
                Left_x_dir.append(pos_x)
                Left_y_dir.append(-pos_y)
            if press_state[1] == "1":
                Right_x_dir.append(pos_x)
                Right_y_dir.append(-pos_y)
            if press_state[2] == "1":
                Mid_x_dir.append(pos_x)
                Mid_y_dir.append(-pos_y)
            All_x_dir.append(pos_x)
            All_y_dir.append(-pos_y)

        '''
        这一段子图借鉴了 FzWjScJ 神的knm 项目地址
        https://github.com/FzWjScJ/knm
        '''
        fig ,axs = plt.subplots(2 ,2)
        
        '''可以根据自己电脑的尺寸修改显示的尺寸'''
        fig.set_figwidth(12)
        fig.set_figheight(10)
        ax1 ,ax2 ,ax3 ,ax4 = axs[0 ,0] ,axs[0 ,1] ,axs[1 ,0] ,axs[1 ,1]
        
        ax1.scatter(All_x_dir ,All_y_dir ,color="hotpink")
        ax1.set_title("ALL")
        ax2.scatter(Right_x_dir ,Right_y_dir ,color="hotpink")
        ax2.set_title("RIGHT")
        ax3.scatter(Left_x_dir ,Left_y_dir ,color="hotpink")
        ax3.set_title("LEFT")
        ax4.scatter(Mid_x_dir ,Mid_y_dir ,color="hotpink")
        ax4.set_title("MID")
        
        plt.show()            

        Get_press_choice = input("需要输出鼠标按键二进制码吗?[y/N](slow):").upper()
        if Get_press_choice == "Y":
            MOUSE.Get_Mouse_press(data_list)
            print("1")

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
        print("-"*50)

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
        plt.scatter(x=x_list ,y=y_list ,c='hotpink')
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
        plt.scatter(x=x_list ,y=y_list ,c='hotpink')
        plt.title("PTH 660")
        plt.show()

class LOG:
    # Logitech, Inc.(0x046d)
    def LOG_Lightspeed_Reveiver(data_list):
        '''
        型号:Lightspeed Receiver(0xc539)
        usbhid.data = 020000130000000000
        头部的02是标识符,相当于是识别的符号
        [2:4]是press  [6:8]是x轴变化  [10:12]是y轴变化
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
        数据结构(usbhid.data):0100fefffeff0000
        [0:2] press   [4:6]  x位移   [8:10]  y位移
        '''
        print("[+] G102 Mouse(0xc09d)")
        changed_list =[]
        for i in data_list:
            i = f"{i[0:2]}{i[4:6]}{i[8:10]}00"
            changed_list.append(i)
        MOUSE.Value_2_plt(changed_list)
    
    def M90_M100_Mouse(data_list):
        '''
        型号: M90/M100 Optical Mouse
        数据结构(usbhid.data):01fefc00
        和普通鼠标是一样的
        '''
        print("[+] M90/M100 Optical Mouse(0xc05a)")
        MOUSE.Value_2_plt(data_list)

    def G402_Gaming_Mouse(data_list):
        '''
        型号: G402 Gaming Mouse (0xc07e)||G102/G203 LIGHTSYNC Gaming Mouse
        数据结构(usbhid.data):0100010001000000
        [0:2] press   [4:6]  x位移   [8:10]  y位移
        '''
        changed_list = []
        for i in data_list:
            i = f"{i[0:2]}{i[4:6]}{i[8:10]}00"
            changed_list.append(i)
        MOUSE.Value_2_plt(changed_list)

    # def G102_G203_Mouse(data_list):
    #     '''
    #     型号: 
    #     数据结构(usbhid.data):0100010001000000
    #     [0:2] press   [4:6] x位移    [8:10]   y位移
    #     '''

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

    def DeathAdder_Mouse(data_list):
        '''
        型号:RZ01-0145, Gaming Mouse [DeathAdder 2000 (Alternate)] (0x004f)
        数据结构(usbhid.data):0006fe000600feff
        [0:2] press  [2:4] x位移 [4:6] y位移
        '''
        print("[+] RZ01-0145, Gaming Mouse [DeathAdder 2000 (Alternate)] (0x004f)")
        changed_list = []
        for i in data_list:
            i = f"{i[0:2]}{i[2:4]}{i[4:6]}00"
            changed_list.append(i)
        MOUSE.Value_2_plt(changed_list)

    def Razer_UnkownType_Mouse(data_list):
        '''
        型号:Unknown (0x0098)
        数据结构(usbhid.data):0101f8000100f8ff
        [0:2] press  [2:4] x位移  [4:6] y位移
        '''
        print("[+] Razer UnknownType Mouse (0x0098)")
        changed_list = []
        for i in data_list:
            i = f"{i[0:2]}{i[2:4]}{i[4:6]}{i[6:8]}"
            changed_list.append(i)
        MOUSE.Value_2_plt(changed_list)

    def Razer_UnkownType_Mouse2(data_list):
        '''
        型号:Unknown (0x0098)
        数据结构(usbhid.data):00000000feff0100
        [0:2] press  [8:10] x位移  [12:14] y位移
        '''
        print("[+] Razer UnknownType Mouse 2 (0x0094)")
        changed_list = []
        for i in data_list:
            i = f"{i[0:2]}{i[8:10]}{i[12:14]}00"
            changed_list.append(i)
        MOUSE.Value_2_plt(changed_list)

class Apple:
    # Apple, Inc.(0x05ac)
    def ANSI(data_list):
        TODO:需要将它改成更合理的数据处理
        '''
        型号:Aluminium Keyboard (ANSI) (0x024f)
        暂且当成普通的键盘来解
        '''
        print("[+] 型号:Apple Aluminium Keyboard (ANSI)(0x024f)\n")
        pad_Keys = {
        "04":"a", "05":"b", "06":"c", "07":"d", "08":"e","09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j","0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o","13":"p", "14":"q", "15":"r", "16":"s", "17":"t","18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y","1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4","22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"\n","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":" ","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>","46":"<PRTSC>","47":"<SCR>","48":"<PAUSE>","49":"<INSERT>","4a":"<HOME>","4b":"<PGUP>","4c":"<DEL FORWARD>","4d":"<END>","4e":"<PGDW>","4f":"<RIGHTARROW>","50":"<LEFTARROW>","51":"<DOWNARROW>","52":"<UPARRWO>","53":"<NUMBERLOCK>","54":"1","55":"*","56":"-","57":"+","58":"<ENTER>","59":"<1/END>","5a":"<2/Down>","5b":"<3/PageDn","5c":"<4/LeftArrow>","5d":"5","5e":"<6/RightArrow>","5f":"<7/Home>","60":"<8/UpArrow>","61":"<9/PageUp>","62":"<0/Insert>","63":"<./Delete>","00":"","":""}
        for i in data_list:
            try:
                i = i.strip("\n")
                print(pad_Keys[i[4:6]] ,end="")
            except:
                continue
        print("\n","-"*50)
        chioce = input("[+] 只需要留下数字键吗？[Y/N]").upper()
        print("\n")
        if chioce == "Y":
            pad_Keys = {
        "04":"a", "05":"b", "06":"c", "07":"d", "08":"e","09":"f", "0a":"g", "0b":"h", "0c":"i", "0d":"j","0e":"k", "0f":"l", "10":"m", "11":"n", "12":"o","13":"p", "14":"q", "15":"r", "16":"s", "17":"t","18":"u", "19":"v", "1a":"w", "1b":"x", "1c":"y","1d":"z","1e":"1", "1f":"2", "20":"3", "21":"4","22":"5", "23":"6","24":"7","25":"8","26":"9","27":"0","28":"\n","29":"<ESC>","2a":"<DEL>", "2b":"\t","2c":" ","2d":"-","2e":"=","2f":"[","30":"]","31":"\\","32":"<NON>","33":";","34":"'","35":"<GA>","36":",","37":".","38":"/","39":"<CAP>","3a":"<F1>","3b":"<F2>", "3c":"<F3>","3d":"<F4>","3e":"<F5>","3f":"<F6>","40":"<F7>","41":"<F8>","42":"<F9>","43":"<F10>","44":"<F11>","45":"<F12>","46":"<PRTSC>","47":"<SCR>","48":"<PAUSE>","49":"<INSERT>","4a":"<HOME>","4b":"<PGUP>","4c":"<DEL FORWARD>","4d":"<END>","4e":"<PGDW>","4f":"<RIGHTARROW>","50":"<LEFTARROW>","51":"<DOWNARROW>","52":"<UPARRWO>","53":"<NUMBERLOCK>","54":"1","55":"*","56":"-","57":"+","58":"<ENTER>","59":"1","5a":"2","5b":"3","5c":"4","5d":"5","5e":"6","5f":"7","60":"8","61":"9","62":"0","63":".","00":"","":""}
            for i in data_list:
                try:
                    i = i.strip("\n")
                    print(pad_Keys[i[4:6]] ,end="")
                except:
                    continue
        print("\n","-"*50)

class Maxxter:
    def Maxxter_OpticalGaming_Mouse(data_list):
        '''
        型号: Optical Gaming Mouse [Xtrem](0x0f97)
        usbhid.data = 0100f97f0000(6 bytes)
        [0:2] press  [4:6] x位移  [6:8] y位移
        '''
        print("[+] 型号: Maxxter Optical Gaming Mouse [Xtrem](0x0f97)")
        changed_datalist = []
        for i in data_list:
            i = f"{i[0:2]}{i[4:6]}{i[6:8]}00"
            changed_datalist.append(i)
        MOUSE.Value_2_plt(changed_datalist)

    def Wireless_Optical_Mouse_ACT(data_list):
        '''
        型号: Wireless Optical Mouse ACT-MUSW-002(0x8366)
        usbhid.data = 0100fbff00(5 bytes)
        [0:2] press  [4:6] x位移  [6:8] y位移
        '''
        print("[+] 型号: Wireless Optical Mouse ACT-MUSW-002(0x8366)")
        changed_datalist = []
        for i in data_list:
            i = f"{i[0:2]}{i[4:6]}{i[6:8]}00"
            changed_datalist.append(i)
        MOUSE.Value_2_plt(changed_datalist)

class Unknown_Type_Device:
    '''
    这个类是专门用来存储特殊或者是没有名字的USBVendor,
    所以我给它取的名字就叫Unknown,函数名也将用它的流量类似什么标准USB流量来命名
    '''

    def Check_Unknown_And_Recover(DesID_List ,profile_data ,Field_Value ,ip ,file ,Company_List):
        if DesID_List[0] in profile_data["Unknown"]:
            Def_Name = profile_data["Unknown"][DesID_List[0]]["Device_DefName"]
            operator.methodcaller(Def_Name ,Field_Value)(Unknown_Type_Device)
            print(1)
            # 询问是否需要爆破所有的值
            Brute_Choice = input("需要爆破所有的数据吗?[y/N](也许会不准确or是报错):").upper()
            if Brute_Choice != "Y":
                END.Message()
                exit(-1)
            else:
                Burteforce(file ,ip ,profile_data ,Company_List)
            
            END.Message()
            exit(-1)
        else:
            return None

    def Wacom_Like_1(Field_Value):
        '''
        设备ID:0x006d  公司ID:0x256c
        流量格式:0ac0a63f37420000161a(usbhid.data)
        [2:4]==c1为有效数据  [4:8] 为x坐标   [8:12] 为y坐标;并且是大端储存
        '''
        print("[+] 类似Wacom的画板")
        xlist ,ylist = [] ,[]
        for data in Field_Value:
            xpos = int(data[4:6] ,16) + int(data[6:8] ,16)*256
            ypos = int(data[8:10] ,16) + int(data[10:12] ,16)*256
            if data[2:4] == "c1":
                xlist.append(xpos)
                ylist.append(-ypos)
        plt.scatter(xlist ,ylist ,c='hotpink')
        plt.show()
        
    def Mouse_Like_1(Field_Value):
        '''
        这是zeror师傅发我的一个流量包
        设备ID:0x2530  公司ID:0x093a
        流量格式:0103fd000300fdff(usbhid.data)
        [0:2] 按键   [2:4] x位移   [4:6] y位移
        '''
        Changed_Value = []
        for i in Field_Value:
            i = f"{i[0:2]}{i[2:4]}{i[4:6]}00"
            Changed_Value.append(i)
        MOUSE.Value_2_plt(Changed_Value)

    def KeyBoard_Like_1(Field_Value):
        '''
        原题:0xGAME2023 notverybadusb 
        这个是 Arduino 的键盘流量，去掉前两位标识符就是正常的键盘流量
        因为可能会不太常见，所以就把它丢到Unknown了，没有专门写一个类
        0200001a0000000000  
        [0:2] 标识符  [2:4] 功能键  [6:8] 按键
        '''
        print(1)
        changed_list = []
        for i in Field_Value:
            i = f"{i[2:4]}00{i[6:8]}0000000000"
            changed_list.append(i)
        KEYBOARD.Value_2_PlainText(changed_list)

def Get_defname(Device_ID:str ,Device_List:list) -> str:
    # 返回查找到对应公司下的产品对应的解密函数名
    for i in Device_List:
        if i["Device_ID"] == Device_ID:
            return i["Device_DefName"]

def Burteforce(file ,ip ,profile_data ,Company_List):
    os.system(f'tshark -r {file} -T fields -Y \"usb.src!=host && usb.src!={ip}\" -e usb.src > temp_ALLIP.out')
    with open("temp_ALLIP.out") as f:
        ALL_IP_List = [i.strip("\n") for i in (list(set(f.readlines()))) if i.strip("\n")[-1] != "0"]
    
    # 判断是否还有数据可以提取
    if len(ALL_IP_List) == 0:
        print("[-] 已经没有数据可以提取")
        END.Message()
        exit(-1)
    print(f"[+] 有如下{ALL_IP_List}IP可以提取数据")

    for Other_ip in ALL_IP_List:
        # 这一段是在读取此IP的数据类型(usbhid.data/usb.capdata)
        print("-"*50 ,f"\n[=] 正在提取 {Other_ip} 地址的数据")
        
        Zero_ip = Other_ip[:-1] + "0"
        os.system(f'tshark -r {file} -T fields -Y "usb.src=={Zero_ip}" -e usb.bInterfaceClass > temp_dataType.out')
        with open("temp_dataType.out") as f: 
            dataType = "".join(t for t in [i.strip("\n") for i in list(set(f.readlines()))])
        if "0x03" in dataType:
            dataType = "usbhid.data"
        else:continue # 由于还没发现usb.capdata的数据,所以遇到不是usbhid.data的直接跳过
        
        # 这段就是把main函数的一部分给套过来了,因为不会递归(
        Field_Value ,ID_List ,DesID_List = GET_START.Build_Cmd_And_Get_Data(file_name=file ,des_IP=Other_ip ,field_name=dataType)

        if len(Field_Value) == 0:
            print(f"[-] 源IP为{ip},字段名称为{dataType}提取出来的数据为空\n" ,"-"*50)
            continue
        Unknown_Type_Device.Check_Unknown_And_Recover(DesID_List ,profile_data ,Field_Value ,Other_ip ,file ,Company_List)

        # 处理目的IP的数据
        if DesID_List[0] in Company_List:
            # 获取配置文件中的类名
            class_name = Company_List[DesID_List[0]]
            # 获取配置文件中的函数名
            Device_List = profile_data[class_name][1:]
            Def_Name = Get_defname(DesID_List[1] ,Device_List)
            # 将获取的函数名和类名实例化并且执行
            operator.methodcaller(Def_Name ,Field_Value)(globals()[class_name])
        # 处理默认值
        else:
            if len(Field_Value[0].strip("\n")) == 8:
                MOUSE.Value_2_plt(Field_Value)
            elif len(Field_Value[0].strip("\n")) == 16:
                KEYBOARD.Value_2_PlainText(Field_Value)
            else:
                print(f"[-] 地址为 {Other_ip} 的数据未能解密\n" ,"-"*50)

def main():
    # 检查系统是否是linux系统
    # if platform.system() == "Linux" or platform.system() == "Darwin":
    #     print(f"[-] 您当前的操作系统{platform.system()},本工具只适用于Linux系统!\n[=] PS:将tshark命令添加到环境变量,再注释main()函数第一个判断语句就可以在windows使用了^^")
    #     exit(-1)
    
    # 读取配置文件
    profile_data = {}

    with open(f"{os.path.split(os.path.realpath(__file__))[0]}/profile.yaml" ,"r" ,encoding="utf-8") as f:
        profile_data = f.read()
        profile_data = yaml.safe_load(profile_data)

    # 从命令行读取流量包的相关数据
    file ,ip ,field = GET_START.Get_Basic_Parameter()
    Field_Value ,ID_List ,DesID_List = GET_START.Build_Cmd_And_Get_Data(file_name=file ,des_IP=ip ,field_name=field)
    print(f"[+] [DEVICE_LIST]: {ID_List}\n[+] 您可以在USB_ID_List.txt中查找具体的设备名称\n" ,"-"*50)

    # 如果返回值有问题，报错并且停止程序
    if len(Field_Value) == 0:
        print(f"[-] 源IP为{ip},字段名称为{field}提取出来的数据为空,请检查一下IP和字段是否正确以及对应IP下是否有数据")
        exit(-1)
    
    # 获取记录的所有公司的ID号
    Company_List = profile_data["Company_List"][0]
    print(Company_List)

    # 判断目的IP是否是Unknown类型的数据,并且解密;
    Unknown_Type_Device.Check_Unknown_And_Recover(DesID_List ,profile_data ,Field_Value ,ip ,file ,Company_List)

    # 处理目的IP的数据
    if DesID_List[0] in Company_List:
        # 获取配置文件中的类名
        class_name = Company_List[DesID_List[0]]
        # 获取配置文件中的函数名
        Device_List = profile_data[class_name][1:]
        Def_Name = Get_defname(DesID_List[1] ,Device_List)
        if Def_Name == None:
            print("[-] 该产品尚未记录在工具中,请练习作者增添该工具")
            exit(-1)
        # 将获取的函数名和类名实例化并且执行
        operator.methodcaller(Def_Name ,Field_Value)(globals()[class_name])
    
    # 处理默认值
    else:
        if len(Field_Value[0].strip("\n")) == 8:
            MOUSE.Value_2_plt(Field_Value)
        elif len(Field_Value[0].strip("\n")) == 16:
            KEYBOARD.Value_2_PlainText(Field_Value)  

    # 询问是否需要爆破所有的值
    Brute_Choice = input("需要爆破所有的数据吗?[y/N](也许会不准确or是报错):").upper()
    if Brute_Choice != "Y":
        END.Message()
        exit(-1)
    
    # 接下来的所有代码就是爆破所有的数据,也不是都能爆破出来,只是给做题的时候提供一点线索(如果有的话)
    Burteforce(file ,ip ,profile_data ,Company_List)
    

    os.remove("temp_dataType.out")
    os.remove("temp_ALLIP.out")
    END.Message()

if __name__ == "__main__":
    main()

    print('[=] wireshark抓包测试')