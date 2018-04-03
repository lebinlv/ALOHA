# coding utf-8
import random
import numpy as np
import matplotlib.pyplot as plt

def aloha(sum_num=1):
    package_length = 1          # 单个包时间长度为1
    total_time = 1000           # 观测时间长度1000
    G_MAX = 3                   # 设定G的最大值
    sum_n = sum_num             # 多次随机求和平均，进行图像拟合，sum_n为求和次数

    G_array = np.zeros(G_MAX*package_length*total_time)     # 初始化G值数组，数组长度为G_MAX*package_length*total_time
    S_array = np.zeros(G_MAX*package_length*total_time)     # 初始化S值数组，数组长度为G_MAX*package_length*total_time
    total_n = G_MAX*package_length*total_time*sum_n         # 完成绘图需要的总计算量，用于计算当前完成度
    processed_n = 0                                         # 当前已完成计算量，初始值为0

    for n in range(1,sum_n+1):  # 此循环将求出sum+1张G、S对应关系图，然后将他们对应相加，即完成了随机平均的求和过程

        # 此循环将得到一对较为粗糙的G、S值
        for idx in range(1,G_MAX*package_length*total_time+1):  # idx表示发送的包的总量
            success = 0             # 成功传送的包的数量，初始值为0
            send_time = []          # 记录每个包的发送时间
        
            # 此循环随机生成每个包的发送时间        
            for i in range(0,idx):
                send_time.append(random.uniform(0,total_time))

            # 对发送时间排序，便于计算包是否有重合
            send_time.sort()

            # 计算成功发送的包的个数
            if idx==1:
                success += 1
            else:
                # 计算每相邻两个包的发送时间的差值，保存在 diff_time 
                diff_time = np.zeros(idx-1)
                for i in range(0,idx-1):
                    diff_time[i] = send_time[i+1]-send_time[i]
                # 对于第一个包，只需判断 第二个包的发送时间 是否大于 第一个报的发送时间+包的长度
                if diff_time[0] > package_length:
                    success += 1
                # 对于中间的包，需要判断两个时间差
                for i in range(1,idx-1):
                    if diff_time[i-1] > package_length and diff_time[i] > package_length:
                        success += 1
                # 对于最后一个包，只需判断 最后一个包的发送时间-倒数第二个包的发送时间 是否大于 包的长度    
                if diff_time[idx-2] > package_length and send_time[idx-1]+package_length < total_time:
                    success += 1
            
            S = success*package_length/total_time             # 计算本次循环中的S值
            G = idx*package_length/total_time                 # 计算本次循环中的G值
            
            G_array[idx-1] += G                               # 求和，完成随机平均的求和过程
            S_array[idx-1] += S

            # 计算当前完成度并输出
            processed_n += 1
            print('\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b%6.2f%% Completed!'%(processed_n*100/total_n),end=' ')

    G_array/=sum_n        # 平均，完成随机平均的平均过程
    S_array/=sum_n

    plt.plot(G_array,S_array)   # 绘图
    plt.show()
    print('\n')
