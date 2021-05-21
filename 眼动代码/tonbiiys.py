#coding:UTF-8
import cv2 as cv
import time
import tobii_research as tr
import numpy as np
from tkinter import *
import os
from PIL import Image, ImageTk
# from multiprocessing import Process
from pymouse import PyMouse
import multiprocessing
import threading
import matplotlib.pyplot as plt
import tkinter as tk           # 导入GUI界面函数库
import json
import codecs
# 设置主界面
root = tk.Tk()
root.title('Wellcome to Eye Tracking Application!')
image2 = Image.open(r'F:\22.jpg')
background_image = ImageTk.PhotoImage(image2)
w = background_image.width()
h = background_image.height()
root.geometry('%dx%d+0+0' % (w, h))

background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# root.geometry('900x660')
# root.resizable(width=False, height=False)
# L1 = Label(root)
# L1.pack(side='right')


# canvas = Canvas(root, width=1700, height=660, bg='SkyBlue')
# # image_file = PhotoImage(file='D:/eyetrack/video_to_pictures/99999.png')
# # image = canvas.create_image(5, 5, anchor='n', image=image_file)
# canvas.pack(side='top')   ！！！！canvas画布会把存完数据，直接显示的图覆盖住了！！！！！
# tk.Label(window, text='Wellcome to Eye Tracking Application!', font=('Tahoma', 30)).place(x=105, y=600)

Label(root, text='Step1 : ', font=('Tahoma', 12)).place(x=300, y=140)
Label(root, text='Step2 : ', font=('Tahoma', 12)).place(x=300, y=200)
Label(root, text='Tep-Tcp Add: ', font=('Tahoma', 12), foreground='black').place(x=38, y=40)
Label(root, text='Base Image Path :', font=('Tahoma', 12), foreground='black').place(x=13, y=90)
Label(root, text='Frequency:Hz', font=('Tahoma', 12), foreground='black').place(x=47, y=140)
Label(root, text='Execution Time :s', font=('Tahoma', 12), foreground='black').place(x=18, y=200)

# 设置输入框entry
Add_tcp = StringVar()
Add_tcp.set('tet-tcp://169.254.4.20')
Add_tcp_1 = Entry(root, textvariable=Add_tcp, font=('Tahoma', 14), width=45).place(x=158, y=40)

'''
Base_image_add = StringVar()
Base_image_add.set('D:/eyetrack/bottom_pictures/777.jpg')
Base_image_add_1 = Entry(root, textvariable=Base_image_add, font=('Tahoma', 14), width=45).place(x=158, y=90)
'''





Frequency = IntVar()
Frequency.set(60)
Frequency_1 = Entry(root, textvariable=Frequency, font=('Tahoma', 14), width=8).place(x=158, y=140)

Execution_Time = IntVar()
Execution_Time.set(15)
Execution_Time_1 = Entry(root, textvariable=Execution_Time, font=('Tahoma', 14), width=8).place(x=158, y=200)

count1 = 0
count2 = 0
count3 = 0
kkk = 0

address = Add_tcp.get()
eyetracker = tr.EyeTracker(address)  # 实际使用眼动仪时一定要打开的注释


# 设置初始化参数
def set_up_parameters():
    global Hz, r, eye_time, screen_width, screen_hight, address, small_w, small_h, list_x_img, list_y_img, list_x_mouse, list_y_mouse, dir_Originalimage, count1, count2, count3

    r = 60  # 中央凹半径的1/2
    screen_width = 1920  # 默认眼动仪的自带屏幕分辨率为:1920*1080
    screen_hight = 1080

    Hz = int(Frequency.get())  # 采样频率
    eye_time = int(Execution_Time.get())  # 眼动执行的总时间
    small_w = int(screen_width * 0.5)  # 在界面显示的宽与高
    small_h = int(screen_hight * 0.5)
    #dir_Originalimage = Base_image_add.get()  # 底图的存放地址

    list_x_img = []  # 存放眼动中央凹的坐标
    list_y_img = []

    list_x_mouse = []  # 存放鼠标跟随眼动的坐标
    list_y_mouse = []

    count1 = 0  # 计数用
    count2 = 0
    count3 = 0

    print('Hz = ', Hz)
    print('r = ', r)
    print('eye_time', eye_time)
    print('screen_width', screen_width)
    print('screen_hight', screen_hight, '___________________________________________________')


# 连接眼动仪
def connect_eyetracker():
    global eye_time
    eye_time = int(Execution_Time.get())  # 从输入框中获取总实验时间
    Hz = int(Frequency.get())  # 从输入框中获取采样频率

    print("Address: " + eyetracker.address)
    print("Model: " + eyetracker.model)
    print("Name (It's OK if this is empty): " + eyetracker.device_name)
    print("Serial number: " + eyetracker.serial_number)
    print("Execution_Time", eye_time)

    eyetracker.set_gaze_output_frequency(60)  # 设置采样频率(Hz)
    initial_gaze_output_frequency = eyetracker.get_gaze_output_frequency()
    print("The eye tracker's initial gaze output frequency is {0} Hz.".format(initial_gaze_output_frequency))

    del_files("D:/eyetrack/pictures_1")
    del_files("D:/eyetrack/pictures_small")
    del_files("D:/eyetrack/txt_x_img")
    del_files("D:/eyetrack/txt_y_img")



def show1(image):
    global img_png
    # var.set('已打开')
    top1 = tk.Toplevel()
    image = Image.open('D:/eyetrack/bottom_pictures/777.jpg')
    img = ImageTk.PhotoImage(image)
    label_Img = tk.Label(root, image=img)
    label_Img.pack()
    #img = cv.cvtColor(np.asarray(image),cv.CoLOR_RGB2BGR)
    # canvas1 = tk.Canvas(top1, width=image.width, height=image.height, bg='blue')
    # canvas1.create_image(0, 0, image=img, anchor='nw')
    # canvas1.create_image(image.width, 0, image=img, anchor='nw')
    # canvas1.pack()
    # top1.mainloop()
    return img
# 创建显示图像按钮

def record_data():  ###### 采集数据，为实时中央凹显示######
    # print('eye_time_work.value', eye_time_work.value)
    print("Subscribing to gaze data for eye tracker with serial number {0}.".format(eyetracker.serial_number))
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    print("llll")

    print(gaze_data_callback)
    time.sleep(eye_time)
    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)


def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    print("aaa")
    print(gaze_data)
    global count1, count2,image
    global global_gaze_data
    global_gaze_data = gaze_data

    '''
     save  gaze_data 
    '''
    jsObj = json.dumps(gaze_data)
    print('dddddd')
    print(jsObj)
    fileObject=open('D:/jsonFile.json','a')
    fileObject.write(jsObj)
    fileObject.close()

  # self.gaze_data=gaze_data
  #   print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
  #       gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
  #       gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
    point_data_left = gaze_data['left_gaze_point_on_display_area']
    point_data_right = gaze_data['right_gaze_point_on_display_area']
    # print("type left", type(point_data_left[0]),"type right", type(point_data_left[1]))

    mmm = 0
    if point_data_left[0] > 0.0000001 and point_data_left[1] > 0.0000001 and point_data_right[0] > 0.0000001 and \
            point_data_right[1] > 0.0000001:

        x1 = int(point_data_left[0] * screen_width)  # 等比例效果
        y1 = int(point_data_left[1] * screen_hight)
        x2 = int(point_data_right[0] * screen_width)
        y2 = int(point_data_right[1] * screen_hight)

    else:
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
    image = Image.open('D:/eyetrack/bottom_pictures/777.jpg')
    show1(image)

    img = cv.cvtColor(np.asarray(image),cv.COLOR_RGB2BGR)
    cv.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
    cv.rectangle(img,(x1,y2),(x2,y1),(0,0,255),2)
    cv.imshow('result',img)
    cv.imwrite('D:/imge'+str(count2) + '.jpg',img)
    count2 = count2 + 1
# 创建打开图像和显示图像函数

def showImage():
    file1='D:/jsonFile.json'
    file1=open(file1,'r',encoding='UTF-8')
    js=file1.read()
    print('lp')
    print(js)
    dict_num=json.loads(js)
    print('hhhhh')
    print(dict_num)
    #gaze_data_callback(dict_num)

btn_Show = tk.Button(root,text='显示图像',command=showImage).place(x=158 ,y=90)


    # point_x = int((x1 + x2) / 2)  # 根据左眼x1,y1 右眼x2,y2坐标，折中得到注视点坐标 point_x, point_y
    # point_y = int((y1 + y2) / 2)
    #
    # global count1, count2
    # list_x_img.append(point_x)  # 将数据放到空数组里
    # list_y_img.append(point_y)
    #
    # # 判断眼动开始。 采集数据的同时筛选数据，为了消除抖动，此处的10是设置的阈值
    # if count1 > 0 and point_x != 0 and point_y != 0 and (list_x_img[count1] - list_x_img[count1 - 1] > 10) and (
    #         list_y_img[count1] - list_y_img[count1 - 1] > 10):
    #     file_handle_x = open('D:/eyetrack/txt_x_img/' + str(count2) + '.txt', mode='w')  # 存放眼动坐标到文件夹里，存储为txt格式
    #     point_x_str = str(point_x)
    #     file_handle_x.write(point_x_str)
    #
    #     file_handle_y = open('D:/eyetrack/txt_y_img/' + str(count2) + '.txt', mode='w')
    #     point_y_str = str(point_y)
    #     file_handle_y.write(point_y_str)
    #
    #     Originalimage = cv.imread(dir_Originalimage)  # 读取底图
    #     Blur_Originalimage = cv.blur(cv.imread(dir_Originalimage), (15, 15))  # 模糊化底图
    #
    #     region = Originalimage[(point_y - r):(point_y + r), (point_x - r):(point_x + r)]  # 根据眼动坐标生成中央凹的小紫框
    #     region1 = Blur_Originalimage[(point_y - r):(point_y + r), (point_x - r):(point_x + r)]
    #     mask = 255 * np.ones(region.shape, region.dtype)
    #     cv.copyTo(region, mask, region1)  # 将小紫色框与底图融合
    #     mixed_clone_image = cv.rectangle(Blur_Originalimage, (point_x - r, point_y - r), (point_x + r, point_y + r),
    #                                      (255, 20, 147), 5)
    #     small_img = cv.resize(mixed_clone_image, (small_w, small_h), interpolation=cv.INTER_CUBIC)
    #     cv.imwrite('D:/eyetrack/pictures_mixed/' + str(count2) + '.jpg', mixed_clone_image)
    #     cv.imwrite('D:/eyetrack/pictures_mixed_small/' + str(count2) + '.jpg', 1477)
    #
    #     img_open = Image.open('D:/eyetrack/pictures_mixed_small/' + str(count2) + '.jpg')  # 在数据录入之后，实时的直接在主界面显示中央凹小紫框图
    #     img = ImageTk.PhotoImage(img_open)
    #     L1.config(image=img)
    #     L1.image = img  # keep a reference
    #     mmm = mmm + 1
    #     print('test-log------- mmm = ', mmm)
    #     count2 = count2 + 1

    # count1 = count1 + 1
    # print("count1 = ", count1, "      valid data count2 = ", count2, "           R = ", r)



def record_data1():  ###### 采集数据，为鼠标实时跟随眼动移动######
    eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback1, as_dictionary=True)

    time.sleep(eye_time)
    eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback1)


def gaze_data_callback1(gaze_data):
    # Print gaze points of left and right eye


    # print("Left eye: ({gaze_left_eye}) \t Right eye: r({gaze_right_eye})".format(
    #     gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
    #     gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
    point_data_left = gaze_data['left_gaze_point_on_display_area']
    point_data_right = gaze_data['right_gaze_point_on_display_area']

    # print("type left", type(point_data_left[0]),"type right", type(point_data_left[1]))

    if point_data_left[0] > 0.0000001 and point_data_left[1] > 0.0000001 and point_data_right[0] > 0.0000001 and \
            point_data_right[1] > 0.0000001:

        x1 = int(point_data_left[0] * screen_width)  # 等比例效果
        y1 = int(point_data_left[1] * screen_hight)
        x2 = int(point_data_right[0] * screen_width)
        y2 = int(point_data_right[1] * screen_hight)

    else:
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0

    point_x = int((x1 + x2) / 2)
    point_y = int((y1 + y2) / 2)

    global count1, count2
    list_x_mouse.append(point_x)
    list_y_mouse.append(point_y)

    if count1 > 0 and point_x != 0 and point_y != 0 and (list_x_mouse[count1] - list_x_mouse[count1 - 1] > 5) and (
            list_y_mouse[count1] - list_y_mouse[count1 - 1] > 5):
        file_handle_x = open('D:/eyetrack/txt_x_mouse/' + str(count2) + '.txt', mode='w')
        point_x_str = str(point_x)
        file_handle_x.write(point_x_str)

        file_handle_y = open('D:/eyetrack/txt_y_mouse/' + str(count2) + '.txt', mode='w')
        point_y_str = str(point_y)
        file_handle_y.write(point_y_str)

        count2 = count2 + 1

    count1 = count1 + 1
    print("count1 = ", count1, "      count2 = ", count2)


def read_txt_data():
    top6 = Toplevel()
    top6.geometry('1050x650')
    top6.resizable(width=False, height=False)
    top6.title('Final Result Display')
    canvas = Canvas(top6, width=1100, height=750, bg='DimGray')
    canvas.pack(side='top')

    L2 = Label(top6)
    L2.place(x=42, y=50)

    ppp = 0
    while True:
        if (os.path.exists('D:/eyetrack/txt_x_img/' + str(ppp) + '.txt') == True) and (
                os.path.exists('D:/eyetrack/txt_y_img/' + str(ppp) + '.txt') == True):

            img_open = Image.open('D:/eyetrack/pictures_mixed_small/' + str(ppp) + '.jpg')
            img1 = ImageTk.PhotoImage(img_open)
            L2.config(image=img1)
            L2.image = img1  # keep a reference
            ppp = ppp + 1
            print('ppp = = = = = ', ppp)
            time.sleep(0.3)
        else:
            continue


def realtime1():  # 实时中央凹显示效果

    # connect_eyetracker()
    # global eye_time_work
    # time_one = multiprocessing.Value("i", max_time_interval)
    # p1 = multiprocessing.Process(target=record_data, args=(eye_time_work,))
    # time.sleep(0.5)
    # t2 = threading.Thread(target = read_txt_data)

    t1 = threading.Thread(target=record_data)  # 用一个子线程来执行
    t1.start()
    # t2.start()
    # record_data()
    print('Func: realtime1 finished !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')


def realtime2():  # 实时鼠标跟随眼动移动效果

    # connect_eyetracker()
    # time_two = multiprocessing.Value("i", max_time_interval)
    pp1 = multiprocessing.Process(target=realtimemouse)  # 用一个子进程来执行
    pp1.start()

    record_data1()
    pp1.terminate()  # 子进程终止


def del_files(path_file):  # 用于初始化时，删除之前的文件夹

    ls = os.listdir(path_file)
    for i in ls:
        f_path = os.path.join(path_file, i)
        # 判断是否是一个目录,若是,则递归删除
        if os.path.isdir(f_path):
            del_files(f_path)
        else:
            os.remove(f_path)


def review_result_small():  # 用于回放功能

    top5 = Toplevel()
    top5.geometry('1050x650')
    top5.resizable(width=False, height=False)
    top5.title('Final Result Display')
    canvas = Canvas(top5, width=1100, height=750, bg='Skyblue')
    canvas.pack(side='top')

    L3 = Label(top5)
    L3.place(x=42, y=50)

    while True:

        global kkk
        img_open = Image.open('D:/eyetrack/pictures_mixed_small/' + str(kkk) + '.jpg')
        img = ImageTk.PhotoImage(img_open)
        L3.config(image=img)
        L3.image = img  # keep a reference
        kkk = kkk + 1
        time.sleep(0.5)

        if os.path.exists('D:/eyetrack/txt_x_img/' + str(kkk) + '.txt') == False:
            kkk = 0
            break
            # root.withdraw()


def thread_review_result_small():  # 用于回放功能

    t3 = threading.Thread(target=review_result_small)  # 用一个子进程来执行
    t3.start()


def realtimemouse():
    # m.click(x, y, button, n)
    # 鼠标点击
    # x, y是坐标位置
    # buttong 1表示左键，2 表示点击右键
    # n点击次数，默认是1次，2表示双击

    # time_each_break2 = time_two.value

    k = 0
    m = PyMouse()

    # 不断地从存储中获取数据，一旦有新的数据，就移动鼠标，完成实时鼠标跟随眼动的效果
    while True:
        if (os.path.exists('D:/eyetrack/txt_x_mouse/' + str(k) + '.txt') == True) and (
                os.path.exists('D:/eyetrack/txt_y_mouse/' + str(k) + '.txt') == True):

            file_handle_x = open('D:/eyetrack/txt_x_mouse/' + str(k) + '.txt', mode='r')
            file_handle_y = open('D:/eyetrack/txt_y_mouse/' + str(k) + '.txt', mode='r')

            point_x_str_read = int(file_handle_x.read())
            point_y_str_read = int(file_handle_y.read())
            m.move(point_x_str_read, point_y_str_read - 150)  # 减掉150是测试时发现的误差
            k = k + 1

        else:
            continue
            # time.sleep(time_each_break2/1000) #单位: /s
        # except IOError:
        #     break


def data_show():  # 根据采集的坐标值，画图

    plt.xlim(0, 1920)
    plt.ylim(0, 1080)

    ax = plt.gca()  # gca:get current axis得到当前轴
    ax.xaxis.set_ticks_position('top')
    ax.invert_yaxis()

    plt.scatter(list_x_img, list_y_img, color='r')
    plt.savefig('D:/eyetrack/pictures_mixed/test2.jpg')
    plt.show()

    III = cv.imread('D:/eyetrack/pictures_mixed/test2.jpg')
    cv.imshow('Data Show', III)


if __name__ == '__main__':  # 设置主要按钮，按下即开始对应的功能演示

    btn_login1 = Button(root, text="  Set up  ", font=('Tahoma 12 bold'), foreground='DarkCyan',
                        command=set_up_parameters, activebackground='BlueViolet').place(x=100, y=260)

    btn_login2 = Button(root, text="Connect Eye Tracker", font=('Tahoma 12 bold'), foreground='blue',
                        command=connect_eyetracker, activebackground='BlueViolet').place(x=370, y=137)

    btn_login3 = Button(root, text="Start Real-time Display", font=('Tahoma 12 bold'), foreground='green',
                        command=realtime1, activebackground='BlueViolet').place(x=370, y=197)

    btn_login4 = Button(root, text="Start Real-time Following Mouse", font=('Tahoma 12 bold'), foreground='green',
                        command=realtime2, activebackground='BlueViolet').place(x=370, y=257)

    btn_login5 = Button(root, text="Review EyeTrack Result", font=('Tahoma 12 bold'), foreground='blue',
                        command=thread_review_result_small, activebackground='BlueViolet').place(x=370, y=360)

    btn_login6 = Button(root, text="Data Show", font=('Tahoma 12 bold'), foreground='blue', command=data_show,
                        activebackground='BlueViolet').place(x=370, y=420)

    # 主窗口循环显示
    mainloop()
