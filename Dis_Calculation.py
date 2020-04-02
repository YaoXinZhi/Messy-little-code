# -*- coding:utf-8 -*-
#! usr/bin/env python3
"""
Created on 02/04/2020 下午1:03 
@Author: xinzhi yao 
"""

import numpy as np
from math import radians, sqrt, fabs, sin, asin, cos
import os
import argparse
import re
import itertools

def Coordinate_Trans(cor: str, min=True, sec=True, pre=5):
    #Degrees minutes seconds
    if sec:
        cor_split = re.split(r'\'|"|′|°|″', cor)
        cor_deg = int(cor_split[0])
        cor_min = int(cor_split[1])
        cor_sec = float(cor_split[2])
        cor_d = cor_deg + cor_min/60 + cor_sec/60/60
    else:
        cor_split = re.split(r'\'|°|′', cor)
        cor_deg = int(cor_split[ 0 ])
        cor_min = int(cor_split[ 1 ])
        cor_d = cor_deg + cor_min / 60
    return round(cor_d, pre)

def Dis_Calculation(a_lon: str, a_lat:str, b_lon:str, b_lat:str):
    a_lon_d = Coordinate_Trans(a_lon)
    a_lat_d = Coordinate_Trans(a_lat)
    b_lon_d = Coordinate_Trans(b_lon)
    b_lat_d = Coordinate_Trans(b_lat)
    dis = Haversin_Dis(a_lon_d, a_lat_d, b_lon_d, b_lat_d)
    return dis

def haversin(theta):
    s = sin(theta / 2)
    return s * s

def Haversin_Dis(lat0, lng0, lat1, lng1):
    EARTH_RADIUS = 6371
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = haversin(dlat) + cos(lat0) * cos(lat1) * haversin(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    return distance

def read_group(group_file: str):
    group_dic = {}
    with open(group_file) as f:
        for line in f:
            l = line.strip().split('\t')
            group_dic[l[0]] = (l[2], l[3])
    return group_dic

def main(group_file: str, out: str):
    group_dic = read_group(group_file)
    group_list = list(group_dic.keys())
    wf = open(out, 'w')
    wf.write('Group1\tGroup2\tDistance(KM)\n')

    for i, v in enumerate(group_list):
        for j in group_list[i+1:]:
            print(v, j)
            lon_a, lat_a = group_dic[v]
            lon_b, lat_b = group_dic[j]
            Dis_ab = Dis_Calculation(lon_a, lat_a, lon_b, lat_b)
            wf.write('{0}\t{1}\t{2:.4f}\n'.format(v, j, Dis_ab))
    wf.close()
    print('Done.')

if __name__ == '__main__':
    #
    # parser = argparse.ArgumentParser(description='get_corpus.')
    # parser.add_argument('-aj', dest='a_lon', type=str, required=True, help='longitude of a group')
    # parser.add_argument('-aw', dest='a_lat', type=str, required=True, help='latitude of a group')
    # parser.add_argument('-bj', dest='b_lon', type=str, required=True, help='longitude of b group')
    # parser.add_argument('-bw', dest='b_lat', type=str, required=True, help='latitude of b group')
    # args = parser.parse_args()
    #
    # dis = Dis_Calculation(args.a_lon, args.a_lat, args.b_lon, args.b_lat)
    #
    # print('Distance {0:.8f}KM.'.format(dis))


    # 下面是个测试

    # 深圳野生动物园
    # lon_a = """22°35'58.48"""""
    # lat_a = """113°58'23.26"""""
    #
    # # 深圳坪山站 相距38.3KM
    # lon_b = """22°41'55.27"""""
    # lat_b = """114°19'51.97"""""
    #


    # dis = Dis_Calculation(lon_a, lat_a, lon_b, lat_b)
    # print('Distance {0:.8f}KM.'.format(dis))

    group_file = 'group.txt'
    out = 'group_dis.txt'
    main(group_file, out)
