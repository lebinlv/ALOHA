# coding utf-8
import random
import numpy as np
import matplotlib.pyplot as plt

def aloha(sum_num=1):
    package_length = 1          # 单个包时间长度为1
    total_time = 1000           # 观测时间长度1000
    G_MAX = 3                   # 设定G的最大值
    sum_n = sum_num             # 多次随机平均，进行图像拟合，sum_n为求和次数

    G_array = np.zeros(G_MAX*package_length*total_time)     # 初始化G值数组，数组长度为G_MAX*package_length*total_time
    S_array = np.zeros(G_MAX*package_length*total_time)     # 初始化S值数组，数组长度为G_MAX*package_length*total_time
    total_n = G_MAX*package_length*total_time*sum_n         # 完成绘图需要的总计算量，用于计算当前完成度

    for n in range(1,sum_n+1):  # 此循环将求出sum+1张G、S对应关系图，然后将他们对应相加，即完成了随机平均的求和过程

        # 此循环将得到一对较为粗糙的G、S值
        for idx in range(1,G_MAX*package_length*total_time+1):  # idx表示发送的包的总量
            success = 0             # 初始化成功传送的包的数量为0
            send_time = []          # 记录每个包的发送时间
        
            for i in range(0,idx):  # 随机生成每个包的发送时间
                send_time.append(random.uniform(0,total_time))

            send_time.sort()

            # 计算成功发送的包的个数
            if idx==1:
                success += 1
            else:
                diff_time = np.zeros(idx-1)
                for i in range(0,idx-1):
                    diff_time[i] = send_time[i+1]-send_time[i]
                if diff_time[0] > package_length:
                    success += 1      
                for i in range(1,idx-1):
                    if diff_time[i-1] > package_length and diff_time[i] > package_length:
                        success += 1    
                if diff_time[idx-2] > package_length and send_time[idx-1]+package_length < total_time:
                    success += 1
            
            S = success*package_length/total_time             # 计算本次循环中的S值
            G = idx*package_length/total_time                 # 计算本次循环中的G值
            
            G_array[idx-1] += G                               # 求和，完成随机平均的求和过程
            S_array[idx-1] += S

            # 计算当前完成度并输出
            print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b%5.2f%% Completed!'%((G_MAX*package_length*total_time*(n-1)+idx)*100/total_n),end=' ')

    G_array/=sum_n                                            # 平均，完成随机平均的平均过程
    S_array/=sum_n
    plt.plot(G_array,S_array)                                 # 绘图
    plt.show()
