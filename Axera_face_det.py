import m3axpi
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from apriltag import Detector
#显示时间
import datetime
import time

#视频播放
import os

import socket
import threading
import serial

# os.system("fbon")
# os.system("ffmpeg -i /thing_ipg/output_video.mp4 -pix_fmt rgba -f fbdev /dev/fb0")
# #os.system("fboff")

#加载模型
m3axpi.load("/face_model/yolov5s.json")
#设置边框的颜色宽度
lcd_width, lcd_height, lcd_channel = 854, 480, 4
fnt = ImageFont.truetype("/home/res/sans.ttf", 20)
#fnt = ImageFont.truetype("/usr/share/fonts/truetype/de.ttf", 20)
img = Image.new('RGBA', (lcd_width, lcd_height), (0,191,255,200))
ui = ImageDraw.ImageDraw(img)
ui.rectangle((20, 20, lcd_width-20, lcd_height-20), fill=(0,0,0,0), outline=(255,255,255,200), width=20)
logo = Image.open("/home/res/logo.png")
img.paste(logo, box=(lcd_width-logo.size[0], lcd_height-logo.size[1]), mask=None)
logo2 = Image.open("/thing_ipg/3.png")
img.paste(logo2, box=(40, 60), mask=None)

#返回的用户ID
user_id=""
#一些标志
flag_tag=1
flag_face=1
flag_ui=0
#二维码的信息：
tag_now=""
tag_re=""
#二维码的nun
tag_num=0
#先显示时间，电量等基本信息
#人脸识别之后，显示用户ID
#人脸识别完成之后再创建apriltaag检测器
#货架上的物品

# #商品名称，商品描述
# thing_name="区域名称:"
# thing_dital="区域介绍:"
# thing_stance="快点带回家吧！！！！"

# #商品的图片
# # 标签和对应的文件路径
# tag_to_path = {
#     "1": "/thing_ipg/kele.jpg",
#     "2": "/thing_ipg/shupian.jpg",
#     "3": "/thing_ipg/paomian.jpg"
# }
#按键重置的标志，检测到tag的识别之后，令key_an=0
#按键处理中，检测到按下即可将key_an设置为1
key_an=1

#按键部分：
try:
    from gpiod import chip, line, line_request
    config = None  # rpi is default value A 0
    
    def gpio(gpio_line=0, gpio_bank="a", gpio_chip=0, line_mode=line_request.DIRECTION_INPUT):
        global config
        if config is not None and gpio_line in config:
            gpio_bank, gpio_chip = config[gpio_line]
        l, c = [32 * (ord(gpio_bank.lower()[0]) - ord('a')) + gpio_line, chip("gpiochip%d" % gpio_chip)]
        tmp = c.get_line(l)
        cfg = line_request()
        cfg.request_type = line_mode
        tmp.request(cfg)
        tmp.source = "GPIO chip %s bank %s line %d" % (gpio_chip, gpio_bank, gpio_line)
        return tmp
    
    def load(cfg=None):
        global config
        config = cfg
except ModuleNotFoundError as e:
    pass
#全局变量的价格
name_g=0.0
price_g=0.0
discount_g=0.0
actual_price=0.0
sum_price=0.0
#设置 GPIO 
#扫码 16 17
#导航18 19
#结账 22 23
#翻页 24 25
#扫码
flag_tag_key=0
#导航
flag_Navigation=0
#结账
flag_Checkout=0
#翻页
flag_Flip=0
# 设置 GPIO 16 为输出模式，并输出低电平
button_pin16 = gpio(16,gpio_chip=2, line_mode=line_request.DIRECTION_OUTPUT)

# 设置 GPIO 17 为输入模式
button_pin17 = gpio(17, gpio_chip=2, line_mode=line_request.DIRECTION_INPUT)

# 设置 GPIO 18 为输出模式，并输出低电平
button_pin18 = gpio(18,gpio_chip=2, line_mode=line_request.DIRECTION_OUTPUT)

# 设置 GPIO 19 为输入模式
button_pin19 = gpio(19, gpio_chip=2, line_mode=line_request.DIRECTION_INPUT)

# 设置 GPIO 20 为输入模式
button_pin20 = gpio(20, gpio_chip=2, line_mode=line_request.DIRECTION_INPUT)

# 设置 GPIO 22 为输入模式
button_pin22 = gpio(22, gpio_chip=2, line_mode=line_request.DIRECTION_INPUT)

import time
#设置各个输出引脚的输出电平
button_pin16.set_value(0)
button_pin18.set_value(0)
def test():
    global flag_tag_key
    global flag_Navigation
    global flag_Checkout
    global flag_Flip
    #检测各个输入引脚的电平状态
    if button_pin17.get_value() == 0:
        flag_tag_key=1
        print(flag_tag_key)
        print("Button17 is pressed")
    elif button_pin19.get_value() == 0:
        flag_Navigation=1
        print("Button19 is pressed")
    elif button_pin20.get_value() == 0:
        flag_Checkout=1
        print("Button20 is pressed")
#     else:
#         print("NULL")
    if button_pin22.get_value() == 0:
        flag_Flip=1
        print("Button22 is pressed")

    time.sleep(1)
    # print(time.asctime())

# while True:
#     test()

ser = serial.Serial("/dev/ttyS1", 9600)  # 连接串口     
# 发送--语音提醒--欢迎使用
ser.write(b"start")
ser.close()
#列表，name, price, discount
Goods = []

#获取当前的商品名，价格，折扣
# "name price discount"
def server():
    global Goods
    global flag_ui
    global sum_price
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.32.15",8001))
    while True:
        server.listen(5)
        conn, addr = server.accept()
        data = conn.recv(1024).decode("UTF-8")
        flag_ui=1
        flag, name, price_str, discount_str = data.strip().split()
        price = float(price_str)
        discount = float(discount_str)
        flag=int(flag)
        print(name)
        print(flag)
        if flag == 1:
            Goods.append([name, price, discount])
            sum_price=sum_price+price*discount
        elif flag == 2:
            Goods.remove([name, price, discount])
            sum_price=sum_price-price*discount
        conn.close()
        print(Goods)

    server.close()
    
fnt_large_30 = ImageFont.truetype("/home/res/sans.ttf", 30)        
fnt_large = ImageFont.truetype("/home/res/sans.ttf", 40)
#显示商品信息，文字
thing_name="商品名:"
thing_dital="价格:"
thing_discount="折扣:"
thing_discount_price="折扣价格:"
thing_count="数量:"
thing_sum="总价："

while True:

    #显示时间
    current_time = datetime.datetime.now()
    #限制显示时间的精度
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    #print(current_time)
    #显示电量
    current_date='电量：98%'
    rgba = img.copy()
    ui = ImageDraw.ImageDraw(rgba)
    #显示时间
    ui.text((40, 40), "%s" % formatted_time, font=fnt, fill=(0, 0, 0, 255))
    #显示电量
    ui.text((700, 40), "%s" % current_date, font=fnt,fill=(0, 0, 0, 255))
    #显示欢迎语
    ui.text((280, 40), "%s" % '欢迎使用智U购智慧购物终端，祝您购物愉快！', font=fnt,fill=(0, 0, 0, 200))
    #按键按下，开启人脸识别事件
    #if 按键按下：
    if(flag_face):
        #人脸识别的提示信息
        face_prompt="请将设备翻转，人脸面向摄像头"
        face_prompt2="在语音提示后即可翻转至正面"
        # 首先，定义一个新的字体对象，指定字体文件路径和字体大小
        fnt_large2 = ImageFont.truetype("/home/res/sans.ttf", 40)
        #模型检测：
        tmp = m3axpi.capture()
#         print(tmp[1], tmp[0])
        rgb = Image.frombuffer("RGB", (tmp[1], tmp[0]), tmp[3])
        #rgba.paste(rgb, box=(0, 0), mask=None) ## camera 320x180 paste 854x480
        res = m3axpi.forward()
        #给出人脸提示信息
        ui.text((187, 180), "%s" % face_prompt, font=fnt_large2,fill=(200, 0, 0, 255))
        ui.text((187, 230), "%s" % face_prompt2, font=fnt_large2,fill=(200, 0, 0, 255))
        server_flag = 1
        if 'nObjSize' in res:
            ui = ImageDraw.ImageDraw(rgba)
            ui.text((0, 0), "fps:%02d" % (res['niFps']), font=fnt)
            for obj in res['mObjects']:
                x, y, w, h = int(obj['bbox'][0]*lcd_width), int(obj['bbox'][1]*lcd_height), int(obj['bbox'][2]*lcd_width), int(obj['bbox'][3]*lcd_height)
                ui.rectangle((x,y,x+w,y+h), fill=None, outline=(255,255,255,255))
                ui.text((x, y), "%s:%02d" % (obj['objname'], obj['prob']*100), font=fnt)
                flag_tag=1
                user_id=obj['objname']
                # "1 1 user_id"
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("192.168.32.175",8001))
                client.send(("1 "+ "1 "+ user_id).encode("UTF-8"))
                recv = client.recv(1024).decode("UTF-8")
                ser = serial.Serial("/dev/ttyS1", 9600)  # 连接串口     
                # 发送--语音提醒--登录成功
                ser.write(b"login")
                ser.close()
                client.close()
                flag_face=0
                
                if server_flag:
                    thread = threading.Thread(target=server)
                    thread.daemon = True  # 设置为守护线程，以确保在主线程结束时自动退出
                    thread.start()
                    print("success")
                    server_flag = 0
                    
    if(flag_tag and ~flag_face):
        #显示用户ID
        # 首先，定义一个新的字体对象，指定字体文件路径和字体大小
        fnt_large = ImageFont.truetype("/home/res/sans.ttf", 40)
        
        # 然后，在使用ui.text()函数时，将新的字体对象传递给font参数
        #ui.text((x, y), "%s:%02d" % (obj['objname'], obj['prob']*100), font=fnt_large)
        #ui.text((40, 60), "尊敬的用户，您好：" , font=fnt_large)
         
        ui.text((90, 70), "%s" % user_id+'用户，您好！', font=fnt_large,fill=(0,255,0,200))
        
        
    #按下识别二维码键：
    #按下按键并以完成人脸识别,开始二维码检测事件,并关闭人脸识别事件
    #key_an,按键按下的标志
    #每一次循环，若按下按键即为1，检测到tag后，设置为0
    
#进行按键检测
#     #设置标志位
#     #扫码
#     flag_tag_key=0
#     #导航
#     flag_Navigation=0
#     #结账
#     flag_Checkout=0
#     #翻页
#     flag_Flip=0
    
#     #扫码
#     flag_tag_key=0
#     #导航
#     flag_Navigation=0
#     #结账
#     flag_Checkout=0
#     #翻页
#     flag_Flip=0
    #如果按下了二维码检测按钮
    test()
#     print(flag_tag_key and flag_tag)
#     print(flag_tag_key)
#     print(flag_tag)
    if(flag_tag_key and flag_tag):
        tmp = m3axpi.capture()
        rgb = Image.frombuffer("RGB", (tmp[1], tmp[0]), tmp[3])
        # rgba.paste(rgb, box=(0, 0), mask=None) ## camera 640*360 paste 854x480
        
        # 创建Apriltag检测器
        detector = Detector()
        rgb_gray = rgb.convert('L')
        rgb_np = np.array(rgb_gray)
        # 在图像中检测Apriltag标签
        tags = detector.detect(rgb_np)
        print(tags)
        # 打印检测到的标签信息 

        ui = ImageDraw.ImageDraw(rgba)
#         #二维码检测
        #ui.text((40, 60), "%s" % user_id, font=fnt)
        for tag in tags:
            #按键设置为0，只识别一帧图片
            #识别到tag了，将key_an设置为0
            #key_an=0
            
#             print("Tag ID:", tag.tag_id)
#             print("Tag Family:", tag.tag_family)
#             print("Tag Center:", tag.center)
#             print("Tag Corners:", tag.corners)
#             print((tag.corners[3][0] * (480 / 360), 480 - tag.corners[3][1] * (480 / 360) ,tag.corners[1][0] * (480 / 360), 480 - tag.corners[1][1] * (480 / 360)))
            flag_tag_key=0
            print("正在测试二维码的识别")
            ui.rectangle((tag.corners[3][0]  * (480 / 360) , 480 - tag.corners[3][1]  * (480 / 360) ,tag.corners[1][0]  * (480 / 360) , 480 - tag.corners[1][1]  * (480 / 360) ), fill=None, outline=(255,0,0,255))
            ui.text((tag.corners[3][0], 480 - tag.corners[3][1]), "%d" % int(tag.tag_id), font=fnt)
#             #获取当前二维码所对应的商品名字
#             tag_now=tag_name[int(tag.tag_id)]
#             #获取当前二维码对应的num，用来传回服务器，获取当前的坐标
            tag_num=int(tag.tag_id)
            # "1 2 tag_num"
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("192.168.32.175",8001))
            client.send(("1 "+ "2 "+ str(tag_num)).encode("UTF-8"))
            client.close()
#             logo = Image.open(tag_to_path[str(tag.tag_id)])
#             img.paste(logo, box=(40, lcd_height-logo.size[1]-40), mask=None)
    
#     #显示商品信息，文字
# thing_name="商品名"
# thing_dital="价格:"
# thing_discount="折扣"
# thing_discount_price="折扣价格"
# thing_count="数量"
    ui.text((45, 130), "%s" % thing_name, font=fnt_large_30,fill=(0, 0, 0, 255))
    ui.text((225, 130), "%s" % thing_dital, font=fnt_large_30,fill=(0, 0, 0, 255))
    ui.text((375, 130), "%s" %thing_discount, font=fnt_large_30,fill=(0, 0, 0, 255))
    ui.text((525, 130), "%s" % thing_discount_price, font=fnt_large_30,fill=(0, 0, 0, 255))
    ui.text((735, 130), "%s" % thing_count, font=fnt_large_30,fill=(0, 0, 0, 255))
    print("flag测试")
    print(flag_tag)
    print(flag_ui)
    print(flag_tag and flag_ui)
    if(flag_tag and flag_ui):
        
        flag_ui=0
        #显示商品ui信息
        
#         ui.text((45, 130), "%s" % thing_name, font=fnt_large_30,fill=(0, 0, 0, 255))
#         ui.text((225, 130), "%s" % thing_dital, font=fnt_large_30,fill=(0, 0, 0, 255))
#         ui.text((375, 130), "%s" %thing_discount, font=fnt_large_30,fill=(0, 0, 0, 255))
#         ui.text((525, 130), "%s" % thing_discount_price, font=fnt_large_30,fill=(0, 0, 0, 255))
#         ui.text((735, 130), "%s" % thing_count, font=fnt_large_30,fill=(0, 0, 0, 255))
        
    #输出总价
#         for item in Goods:
#             global name_g
#             global price_g
#             global discount_g,actual_price
#             global actual_price,sum_price
#             global sum_price
#             name_g, price_g, discount_g = item
#             # 处理每一行数据
#             print("计算总价")
#             print(name_g)
#             actual_price = price_g * discount_g
#             sum_price=sum_price+actual_price
#         #总价thing_sum
    ui.text((444, 390), "%s" % thing_sum, font=fnt_large_30,fill=(0, 0, 0, 200))
         #总价price_sum
    print("总价")
    print(sum_price)
    sum_price = round(sum_price, 2)
    ui.text((544, 390), "%s" % str(sum_price), font=fnt_large_30,fill=(0, 0, 0, 200))
        
        # 迭代列表中的每一行数据，计算出总价格
#     for item in Goods:
#         global name_g
#         global price_g
#         global discount_g,actual_price
#         global actual_price,sum_price
#         global sum_price
#         name_g, price_g, discount_g = item
#         # 处理每一行数据
#         actual_price = price * discount
#         sum_price=sum_price+actual_price
        #print(f"Name: {name}, Price: {price}, Discount: {discount}")  
    #获取完当前的名称，价格，折扣，数量后，开始输出
    #获取有多少个元素
    num_rows = len(Goods)
    #循环依次打印获取的商品名称
    print("商品测试")
    print(num_rows)
    if num_rows <= 3:
        print("商品少于3的输出")
        # 行数小于等于3，依次输出
        for i in range(num_rows):
            name, price, discount = Goods[i]
            actual_price = price * discount
            actual_price = round(actual_price, 2)
            # 根据行数确定输出位置
            y_pos = 160 + i * 30
            ui.text((50, y_pos), "%s"%name, font=fnt,fill=(0, 0, 0, 255))
            ui.text((230, y_pos), "%s"%str(price), font=fnt,fill=(0, 0, 0, 255))
            ui.text((380, y_pos), "%s"%str(discount), font=fnt,fill=(0, 0, 0, 255))
            ui.text((530, y_pos), "%s"%str(actual_price), font=fnt,fill=(0, 0, 0, 255))
            ui.text((740, y_pos), "1", font=fnt,fill=(0, 0, 0, 255))
            
    else:
        # 行数大于3，覆盖输出
        start_index = num_rows%3
        for i in range(start_index, num_rows):
            name, price, discount = Goods[i % num_rows]
            actual_price = price * discount
            actual_price = round(actual_price, 2)
            # 根据行数确定输出位置
            y_pos = 160 + (i - start_index) * 30
            ui.text((50,y_pos), "%s"%name, font=fnt,fill=(0, 0, 0, 255))
            ui.text((230,y_pos), "%s"%str(price), font=fnt,fill=(0, 0, 0, 255))
            ui.text((380,y_pos), "%s"%str(discount), font=fnt,fill=(0, 0, 0, 255))
            ui.text((530,y_pos), "%s"%str(actual_price), font=fnt,fill=(0, 0, 0, 255))
            ui.text((740,y_pos), "1", font=fnt,fill=(0, 0, 0, 255))
#     #输出总价
#     #总价thing_sum
#     ui.text((444, 410), "%s" % thing_sum, font=fnt_large_30,fill=(255, 0, 0, 255))
#     #总价price_sum
#     ui.text((534, 410), "%s" % str(sum_price), font=fnt_large_30,fill=(255, 0, 0, 255))
    
    
    
    #防止闪烁，睡眠一会
    m3axpi.display([lcd_height, lcd_width, lcd_channel, rgba.tobytes()])
    #语音导航事件
    if(flag_Navigation):
        #print("导航")
        #导航事件
        ser = serial.Serial("/dev/ttyS1", 9600)  # 连接串口     
        # 发送--语音提醒
        ser.write(b"open")
        while True:
            # 等待一段时间确保数据已经发送到串口
            time.sleep(0.1)
            # 读取串口接收到的数据
            data = ser.read(ser.in_waiting)
            if data:
                data_str = data.decode("utf-8")  # 将字节数据解码为字符串
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(("192.168.32.175",8001))
                if data_str == "1":
                    # "薯片"
                    client.send(("1 "+ "4 "+ "1").encode("UTF-8"))
                elif data_str == "2":
                    # "饮料"
                    client.send(("1 "+ "4 "+ "2").encode("UTF-8"))
                # 关闭串口连接 socket连接
                client.close()
                ser.close()
                break

    #结账事件
    if(flag_Checkout):
        #结算事件
        #print("结账")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("192.168.32.175",8001))
        client.send(("1 "+ "3").encode("UTF-8"))
        client.close()
    
    #tishiri
    
    print(Goods)
    #sum_price=0
    #扫码
    flag_tag_key=0
    #导航
    flag_Navigation=0
    #结账
    flag_Checkout=0
    #翻页
    flag_Flip=0
    time.sleep(0.40)
 