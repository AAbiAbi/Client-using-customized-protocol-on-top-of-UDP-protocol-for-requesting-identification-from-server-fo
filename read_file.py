# -*- coding: cp936 -*-
import re
import linecache
import numpy as np
import os

filename = 'Verification_Database.txt'


# ��ֵ�ı��ļ�ת��Ϊ˫�б���ʽ[[...],[...],[...]],����̬��ά����
# Ȼ��˫�б���ʽͨ��numpyת��Ϊ���������ʽ
def txt_strtonum_feed(filename,client_num):
    data = []
    with open(filename, 'r') as f:  # with����Զ�����close()����
        line = f.readline()
        i = 0
        while i < client_num:
            i = i + 1
            read_data = []
            eachline = line.split(",")  ###���ж�ȡ�ı��ļ���ÿ���������б���ʽ����
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
            # read_data = [eachline[0] ,int(eachline[1]), int(eachline[2])]  # TopN�����ַ�ת��Ϊfloat��
            # lable = []  # lableת��Ϊint��
            # print("lable", len(lable))
            # read_data.append(lable[0])
            # print(read_data)
            # read_data = list(map(float, eachline))
            data.append(read_data)
            # data.append(eachline[1])
            # data.append(eachline[2])
            line = f.readline()
        return data  # ��������Ϊ˫�б���ʽ

if __name__ == '__main__':
    test_content = txt_strtonum_feed('Verification_Database.txt',3)
    print(test_content)
    # print(test_content[1][1])

    # content = np.array(test_content)
    # print(content)  # ����������ʽ
    print(len(test_content))
    # print(test_content)  # ��ά�б�



# # ��ֵ�ı��ļ�ֱ��ת��Ϊ����������ʽ������
# def txt_to_matrix(filename):
#     file = open(filename)
#     lines = file.readlines()
#     # print lines
#     # ['0.94\t0.81\t...0.62\t\n', ... ,'0.92\t0.86\t...0.62\t\n']��ʽ
#     rows = len(lines)  # �ļ�����
#
#     datamat = np.zeros((rows, 3))  # ��ʼ������
#
#     row = 0
#     for line in lines:
#         line = line.strip().split('\t')  # strip()Ĭ���Ƴ��ַ�����β�ո���з�
#         datamat[row, :] = line[:]
#         row += 1
#
#     return datamat
#
#
# # ��ֵ�ı��ļ�ֱ��ת��Ϊ����������ʽ������
# def text_read(filename):
#     # Try to read a txt file and return a matrix.Return [] if there was a mistake.
#     try:
#         file = open(filename, 'r')
#     except IOError:
#         error = []
#         return error
#     content = file.readlines()
#
#     rows = len(content)  # �ļ�����
#     datamat = np.zeros((rows, 3))  # ��ʼ������
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







