import yaml
from USBFlow_Soer import *

'''
添加设备的模板,注意:需要添加到对应的公司
如果列表中没有该公司,需要手动加公司的ID和Name,
如果时间紧急,可以直接将流量的压缩包发到y1shin@163.com就行,谢谢师傅的支持

  - Device_ID: ""
    Device_Name: ""
    Device_Type: ""
    Device_DefName: ""

添加的时候请师傅注意大小写和缩进;
添加完成只需要工具目录下执行一次即可

如果是未添加过的Unknown的设备,如下是添加新设备的模版
    "Company_ID": 
      Company_ID: ""
      Device_ID: ""
      Device_Type: ""
      Device_DefName: ""
'''

des_dir = '''
Company_List: 
  - "0x046d": "LOG"
    "0x056a": "WACOM"
    "0x1532": "Razer"
    "0x05ac": "Apple"
    "0x18f8": "Maxxter"
    "0x248a": "Maxxter"
LOG:
  - Company_ID: "0x046d"
    Company_name: "Logitech, Inc."

  - Device_ID: "0xc539"
    Device_Name: "Lightspeed Receiver"
    Device_Type: "Mouse"
    Device_DefName: "LOG_Lightspeed_Reveiver"

  - Device_ID: "0xc07e"
    Device_Name: "G402 Gaming Mouse"
    Device_Type: "Mouse"
    Device_DefName: "G402_Gaming_Mouse"

  - Device_ID: "0xc08b"
    Device_Name: "Logitech G502 SE HERO Gaming Mouse"
    Device_Type: "Mouse"
    Device_DefName: "LOG_G502_MOUSE"

  - Device_ID: "0xc077"
    Device_Name: "Logitech Mouse"
    Device_Type: "Mouse"
    Device_DefName: "Mouse"

  - Device_ID: "0xc341"
    Device_Name: "Logitech Unknow Keyboard Type"
    Device_Type: "KeyBoard"
    Device_DefName: "Unknown_keyboard"

  - Device_ID: "0xc53f"
    Device_Name: "G304 Wireless"
    Device_Type: "Mouse"
    Device_DefName: "G304_Wireless"

  - Device_ID: "0xc09d"
    Device_Name: "G102 Wire"
    Device_Type: "Mouse"
    Device_DefName: "G102_Wire"

  - Device_ID: "0xc05a"
    Device_Name: "M90/M100 Optical Mouse"
    Device_Type: "Mouse"
    Device_DefName: "M90_M100_Mouse"

  - Device_ID: "0xc092"
    Device_Name: "G102/G203 LIGHTSYNC Gaming Mouse"
    Device_Type: "Mouse"
    Device_DefName: "G402_Gaming_Mouse"

Maxxter:
  - Company_ID: "0x18f8"
    Company_name: "Maxxter"

  - Device_ID: "0x0f97"
    Device_Name: "Optical Gaming Mouse [Xtrem]"
    Device_Type: "Mouse"
    Device_DefName: "Maxxter_OpticalGaming_Mouse"

  - Device_ID: "0x8366"
    Device_Name: "Wireless Optical Mouse ACT-MUSW-002"
    Device_Type: "Mouse"
    Device_DefName: "Wireless_Optical_Mouse_ACT"

WACOM:
  - Company_ID: "0x056a"
    Company_name: "Wacom Co., Ltd"

  - Device_ID: "0x030e"
    Device_Name: "CTL-480 [Intuos Pen (S)]"
    Device_Type: "wacom"
    Device_DefName: "CTL_480"

  - Device_ID: "0x0357"
    Device_Name: "PTH-660 [Intuos Pro (M)]"
    Device_Type: "wacom"
    Device_DefName: "PTH_660"

Razer:
  - Company_ID: "0x1532"
    Company_name: "Razer USA, Ltd"
  
  - Device_ID: "0x0083"
    Device_Name: "RC30-0315, Gaming Mouse [Basilisk x HyperSpeed]"
    Device_Type: "Mouse"
    Device_DefName: "Basilisk_Mouse"

  - Device_ID: "0x004f"
    Device_Name: "RZ01-0145, Gaming Mouse [DeathAdder 2000 (Alternate)]"
    Device_Type: "Mouse"
    Device_DefName: "DeathAdder_Mouse"

  - Device_ID: "0x0098"
    Device_Name: "Razer UnknownType Mouse"
    Device_Type: "Mouse"
    Device_DefName: "Razer_UnkownType_Mouse"

  - Device_ID: "0x0094"
    Device_Name: "Razer UnknownType Mouse 2"
    Device_Type: "Mouse"
    Device_DefName: "Razer_UnkownType_Mouse2"

Apple:
  - Company_ID: "0x05ac"
    Company_name: "Apple, Inc."

  - Device_ID: "0x024f"
    Device_Name: "Aluminium Keyboard (ANSI)"
    Device_Type: "KeyBoard"
    Device_DefName: "ANSI"

HP:
  - Company_ID: "0x03f0"
    Company_name: "HP, Inc"



Unknown:
    "0x256c": 
      Company_ID: "0x256c"
      Device_ID: "0x006d"
      Device_Type: "Wacom Like"
      Device_DefName: "Wacom_Like_1"

    "0x093a":
      Company_ID: "0x093a"
      Device_ID: "0x2530"
      Device_Type: "Mouse Like"
      Device_DefName: "Mouse_Like_1"

    "0x2341": 
      Company_ID: "0x2341"
      Device_ID: "0x8036"
      Device_Type: "Keyboard Like"
      Device_DefName: "KeyBoard_Like_1"

Default:
  - type: "Mouse"
    datalen: 8
    name: "Default Mouse"
  - type: "KeyBoard"
    datalen: 16
    name: "Default KeyBoard"
'''
dict_var = yaml.safe_load(des_dir)
with open("./profile.yaml" ,"w" ,encoding="utf-8") as f:
    yaml.dump(dict_var ,f ,default_flow_style=False)
print("[+] 更新profile.yaml成功")
