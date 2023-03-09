# -*- coding: cp936 -*-
import re
import linecache
import numpy as np
import os

filename = 'Verification_Database.txt'


# 数值文本文件转换为双列表形式[[...],[...],[...]],即动态二维数组
# 然后将双列表形式通过numpy转换为数组矩阵形式
def txt_strtonum_feed(filename,client_num):
    data = []
    with open(filename, 'r') as f:  # with语句自动调用close()方法
        line = f.readline()
        i = 0
        while i < client_num:
            i = i + 1
            read_data = []
            eachline = line.split(",")  ###按行读取文本文件，每行数据以列表形式返回
            # print(eachline)
            # print(eachline[0])
            phone_num = int(eachline[0])
            tech_pro  = int(eachline[1])
            is_pay = int(eachline[2])
            read_data.append(phone_num)
            read_data.append(tech_pro )
            read_data.append(is_pay)
            # print("eachline", len(eachline), eachline[0])
            # print(eachline[1])
            # print(eachline[2])
            # print(eachline[3])
            # read_data = [eachline[0] ,int(eachline[1]), int(eachline[2])]  # TopN概率字符转换为float型
            # lable = []  # lable转换为int型
            # print("lable", len(lable))
            # read_data.append(lable[0])
            # print(read_data)
            # read_data = list(map(float, eachline))
            data.append(read_data)
            # data.append(eachline[1])
            # data.append(eachline[2])
            line = f.readline()
        return data  # 返回数据为双列表形式

if __name__ == '__main__':
    test_content = txt_strtonum_feed('Verification_Database.txt',3)
    print(test_content)
    # print(test_content[1][1])

    # content = np.array(test_content)
    # print(content)  # 矩阵数组形式
    print(len(test_content))
    # print(test_content)  # 二维列表



# # 数值文本文件直接转换为矩阵数组形式方法二
# def txt_to_matrix(filename):
#     file = open(filename)
#     lines = file.readlines()
#     # print lines
#     # ['0.94\t0.81\t...0.62\t\n', ... ,'0.92\t0.86\t...0.62\t\n']形式
#     rows = len(lines)  # 文件行数
#
#     datamat = np.zeros((rows, 3))  # 初始化矩阵
#
#     row = 0
#     for line in lines:
#         line = line.strip().split('\t')  # strip()默认移除字符串首尾空格或换行符
#         datamat[row, :] = line[:]
#         row += 1
#
#     return datamat
#
#
# # 数值文本文件直接转换为矩阵数组形式方法三
# def text_read(filename):
#     # Try to read a txt file and return a matrix.Return [] if there was a mistake.
#     try:
#         file = open(filename, 'r')
#     except IOError:
#         error = []
#         return error
#     content = file.readlines()
#
#     rows = len(content)  # 文件行数
#     datamat = np.zeros((rows, 3))  # 初始化矩阵
#     row_count = 0
#
#     for i in range(rows):
#         content[i] = content[i].strip().split('\t')
#         datamat[row_count, :] = content[i][:]
#         row_count += 1
#
#     file.close()
#     return datamat
#







