# USBFlow_Soer
Usage : python3 USBFlow_Soer.py -f filename -p usb.src -d [usbhid.data/usb.capdata]

  这个项目的原理是通过USBid的唯一性，来写出特定的数据解析脚本，本质上是穷举的做法，师傅们如果遇到了什么特殊的USB流量或者是对这个项目有什么建议，
  欢迎与我QQ:`2729913542`交流，基本上能做到秒回(づ￣ 3￣)づ。
  本项目基于tshark建造，请确保linux中下载有tshark.

  由于不知道为什么有些demo上传不进去，于是就上传到网盘了:`https://pan.baidu.com/s/1qEL3mfSJLOBig0tSq9UV7Q?pwd=love`如果需要的话，烦请师傅手动下一下

  更新日志1:在zeror师傅的指导下，对代码进行了重构，现在添加新设备将更加简单和易懂；
  由于本工具原理是穷举，所以难免会出现解密不了的数据，届时，还烦请师傅您将流量包发到邮箱`y1shin@163.com`谢谢师傅您的支持

  更新日志2:修复若干bug，如果想要在windows下使用，只需要想办法在windows下执行tshark命令即可，再将main()函数的第一个判断语句删掉即可

  更新日志3:借鉴了knm的鼠标的显示模式，分成左右中总四块分别显示



>Q&A:

>  Q1.为什么没有什么数据都没有提出来？

>  A: 检查tshark版本，4.0以上为好 `sudo apt-get update|sudo apt-get install tshark` 

>  Q2.为什么Windows不能用？

>  A: 因为windows下没有tshark，所以需要先安装tshark，因为windows下的tshark是`exe`文件，所以需要手动添加tshark路径，或者是将`tshark.exe`添加到环境变量中
