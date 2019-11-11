# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 19:55:43 2016
计算目标函数的第二种方法，在计算经过的格网时采用了缓存的方法~~
@author: dell
"""

import time
import psycopg2
import copy
import pandas as pd
import numpy as np

#获得数组中高于均值三倍标准差的离群点的个数
def getOutliersNum(density_array):
    outliers = 0
    N = len(density_array)
    narray = np.array(density_array)
    mean = narray.mean()
    stdev = narray.std()
      
    for i in range(N):
        if (density_array[i]-mean) > stdev * 9:
            outliers += 1
            
    return outliers

#目标函数
def objFunction(individual):
    
    #参数赋值
    vardim = individual.vardim
    chrom = individual.features
    hos_opt_id_arr = individual.hos_opt
    
    #数据库连接参数
    conn=psycopg2.connect(database='BJT2013',user='postgres',password = '123456',host='localhost',port='5432')
    cur=conn.cursor()
    
    #hos_can_id_arr 存储获得候选医院的属性,已换成五环之外的数据点0731
    hos_can_id_arr = []
    lines = open("e:\\0000\\hos_can_beyond5ring.txt",'r').readlines()
    for i in range(1,len(lines)):
        hos_can_id_arr.append(int(lines[i].strip().split(',')[2]))
    
    #grid_density hos_opt 存储最终需要统计优化的量及优化的医院
    P = vardim #代表着需要优化的医院数目
    grid_density = [0]*8748
                  
    # where_taxi_cover_matrix  hos_index 原始的病人分布及医院下标
    lines = open("E:\\0000\\whereTaxiCoverResearch.txt",'r').readlines()
    where_taxi_cover_matrix = [[] for row in range(8748)]
    hos_index = []
    for i in range(1,len(lines[0].strip('\n').split(','))):
        hos_index.append(int(lines[0].strip('\n').split(',')[i]))
    for i in range(1,len(lines)):
        data = lines[i].strip('\n').split(',')
        for j in range(1,len(data)):
            where_taxi_cover_matrix[int(data[0])].append(int(data[j]))
    
    '''
    上文中得到的数据为where_taxi_cover_matrix，作为原始的数据输入
    该部分计算搬迁了P家医院之后的病人分布
    输入数据为：P值，即变量的维度vardim，还有染色的长度chrom
    输出数据为： temp_where_taxi_from_matrix
    需要叠加多家医院的新情形
    '''        
    #对象拷贝，深拷贝
    temp_where_taxi_from_matrix = copy.deepcopy(where_taxi_cover_matrix)        
    #获得P家医院搬迁之后的病人分布        
    for order in range(P):
        #寻找到ID为医院ID的数据在第几列
        for i in range(len(hos_index)):
            if(hos_index[i] == hos_opt_id_arr[order]):
                opt_idx = i
                break
        #
        for j in range(len(temp_where_taxi_from_matrix)):
            if(temp_where_taxi_from_matrix[j][opt_idx]) !=0:
                
                #分析待优化医院搬迁之后【未带走】的病源的新分布（频率最高原则）
                selectSql = "SELECT hos0,hos1,hos2 FROM frequency_top5 WHERE fid = '%d'"%(j)
                cur.execute(selectSql)
                for record in cur:
                    first_hos_id = record[0]
                    second_hos_id = record[1] #不能int(),可能为空值，下面判断
                    third_hos_id = record[2]
                    
                #如果次数最高的医院不是需要优化的医院本身
                if first_hos_id != None and first_hos_id != hos_opt_id_arr[order]:
                    for k in range(len(hos_index)):
                        if hos_index[k] ==  first_hos_id:
                            first_hos_idx = k
                            break
                    temp_where_taxi_from_matrix[j][first_hos_idx] += \
                    int(0.3*temp_where_taxi_from_matrix[j][opt_idx])
                    
                elif second_hos_id != None and first_hos_id == hos_opt_id_arr[order] \
                and  second_hos_id != hos_opt_id_arr[order]:
                    for k in range(len(hos_index)):
                        if hos_index[k] == second_hos_id:
                            sec_hos_idx = k
                            break
                    temp_where_taxi_from_matrix[j][sec_hos_idx] += \
                    int(0.3*temp_where_taxi_from_matrix[j][opt_idx])
                elif third_hos_id != None and  first_hos_id == hos_opt_id_arr[order] \
                and second_hos_id == hos_opt_id_arr[order] and third_hos_id !=hos_opt_id_arr[order]:
                    for k in range(len(hos_index)):
                        if hos_index[k] == third_hos_id:
                            third_hos_idx = k
                            break
                    temp_where_taxi_from_matrix[j][third_hos_idx] += \
                    int(0.3*temp_where_taxi_from_matrix[j][opt_idx])
                else:
                    selectSql = "SELECT hos0,hos1 FROM distance_top5 WHERE fid = '%d'"%(j)
                    cur.execute(selectSql)
                    for record in cur:
                        nearest_hos_id = record[0]
                        sec_nearest_hos_id = record[1]
                    if nearest_hos_id != None and nearest_hos_id != hos_opt_id_arr[order]:
                        for k in range(len(hos_index)):
                            if hos_index[k] == nearest_hos_id:
                                nearest_hos_idx = k
                                break
                        temp_where_taxi_from_matrix[j][nearest_hos_idx] += \
                        int(0.3*temp_where_taxi_from_matrix[j][opt_idx])
                    elif sec_nearest_hos_id != None and sec_nearest_hos_id != hos_opt_id_arr[order]:
                        for k in range(len(hos_index)):
                            if hos_index[k] == sec_nearest_hos_id:
                                sec_nearest_hos_idx = k
                                break
                        temp_where_taxi_from_matrix[j][sec_nearest_hos_idx] += \
                        int(0.3*temp_where_taxi_from_matrix[j][opt_idx])
                
                #分析待优化医院搬迁之后【带走的】病源给新医院增加的病人分布
                for k in range(len(hos_index)):
                    if hos_index[k] == hos_can_id_arr[int(chrom[order])]:
                        can_idx = k
                        break
                temp_where_taxi_from_matrix[j][can_idx] += \
                int(0.7*temp_where_taxi_from_matrix[j][opt_idx])
                #清空原始的分布为0
                temp_where_taxi_from_matrix[j][opt_idx] = 0
                
    #print("get the new pattern,time is  "+ time.strftime("%H:%M:%S"))
    
    '''
    上文得到的数据为temp_where_taxi_from_matrix，实际是需要优化的多家医院的叠加
    计算新的分布下医院的带来的交通量的情况
    输入数据为temp_where_taxi_from_matrix矩阵，其中存储了医院的病人来源情况
    输出数据为 grid_density，统计新的分布下的路网压力
    需要单独计算每一家医院带来的交通量的总和然后再累加
    '''
    for m in range(len(temp_where_taxi_from_matrix)):
        for n in range(len(temp_where_taxi_from_matrix[0])):
            grid_to_hos_num = temp_where_taxi_from_matrix[m][n]
            if grid_to_hos_num != 0:
                selectSql = "SELECT line_cross FROM grid_to_hos_cache_table_new WHERE \
                             grid_id = '%d' and hos_id = '%d'"%(m,hos_index[n])
                cur.execute(selectSql)
                records = cur.fetchall()
                for record in records:
                    potential_grid_set = record[0].split(',')
                #potential_grid_set = re.sub('{|}','',open("E:\\0000\\cache\\"+str(m)+'to'+str(hos_index[n])+'.txt','r').readline()).split(',')
                for temp_id in potential_grid_set:
                    grid_density[int(temp_id)] += grid_to_hos_num
                    
    '''
    上文中得到的数据为 grid_density，下面将计算目标函数的值
    输入数据为：grid_density计算格网行车数量，temp_where_taxi_from_matrix 病人分布，格网与每家医院的距离
    输出数据为：目标方程的值
    '''
    #计算平均距离--可达性
    grid_to_hos_dis = pd.read_csv("E:\\0000\\distance\\gridToHosDisAll.txt",sep = ',',header= None)
    grid_to_hos_dis = grid_to_hos_dis.values[0:8748,1:167]
    temp_where_taxi_from_array = np.array(temp_where_taxi_from_matrix)
    distance_array = grid_to_hos_dis*temp_where_taxi_from_array
    temp_average_distance = distance_array.sum()/temp_where_taxi_from_array.sum()
    
    #计算格网的离群点数目
    grid_outliers = getOutliersNum(grid_density)
    
    #原始格网的数值
    #original_ave_dis = 4813.47756651
    #original_grid_outliers = 23
    #按照比例计算
    #dis_ratio = temp_average_distance/4813.47756651
    #outlier_ratio = float(grid_outliers)/23
    
    #print("优化的医院ID为："+str(hos_opt_id_arr[0:vardim]))
    #print("平均距离为："+str(temp_average_distance))
    #print('离群点数目：'+str(grid_outliers))
    
    
    return temp_average_distance,grid_outliers,grid_density

                  
                
                
        
