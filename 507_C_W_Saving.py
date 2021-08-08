
from itertools import product
from math import sqrt
from math import pi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import csv

# Parameters

StartCity = 0

EndCity = 0

Vcap = 20

#no_city = 6
#no_city = 11
#no_city = 16
no_city = 26

#city_list = [1,2,3,4,5,6]
#city_list = [1,2,3,4,5,6,7,8,9,10,11]
#city_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
city_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

#numv = 6
#numv = 11
#numv = 16
numv = 26

#Q = [0,7,14,4,8,3,5,12,13,3,21,25,18]

#distance = pd.read_csv('distance.csv')
#distance = pd.read_csv('2distance.csv')
#distance = pd.read_csv('3distance.csv')
distance = pd.read_csv('4distance.csv')
distance_matrix = np.asarray(distance)

#demand = pd.read_csv('demand.csv')
#demand = pd.read_csv('2demand.csv')
#demand = pd.read_csv('3demand.csv')
demand = pd.read_csv('4demand.csv')
Q = np.asarray(demand)

#batterylv = pd.read_csv('battery.csv')
#batterylv = pd.read_csv('2battery.csv')
#batterylv = pd.read_csv('3battery.csv')
batterylv = pd.read_csv('4battery.csv')
batterylevel = np.asarray(batterylv)

City = range(no_city)

Q_Sorted = np.sort(Q)[::-1]
Q_Sorted = np.asmatrix(Q_Sorted)
max_Q = max(Q)


totQ=0
for i in City:
    totQ += Q[i]

numRoute = np.ceil(totQ/Vcap)

# Compute key parameters of MIP model formulation
number_point = no_city
cartesian =list(product(range(number_point),range(number_point)))


savings = np.zeros((number_point,number_point))
for i in range(number_point):
    for j in range(number_point):
        if i!=j:
            savings[i,j]=distance_matrix[StartCity,i]+distance_matrix[StartCity,j]-distance_matrix[i,j]

savings = np.zeros((number_point,number_point))
for i in range(number_point):
    for j in range(number_point):
        if i<j:
            savings[i,j]=distance_matrix[StartCity,i]+distance_matrix[StartCity,j]-distance_matrix[i,j]

# Nihai Kod
def cw(i, j):
    sonuc = distance_matrix[StartCity,i]+distance_matrix[StartCity,j]-distance_matrix[i,j]
    return sonuc
cw_saving = {(i,j): cw(i,j) for i,j in cartesian if i<j and i!=StartCity}

cw_saving_sort=sorted(cw_saving.items(), key=lambda x: x[1], reverse=True)

for i in cw_saving_sort:
    print(i[0],i[1])
    print(city_list[i[0][0]],city_list[i[0][1]],i[1])
    print(i[0][0],i[0][1],i[1],Q[i[0][0]],Q[i[0][1]])
    
cw_saving_sort_matrix = []
for i in cw_saving_sort:
    abc = [i[0][0],i[0][1],i[1],Q[i[0][0]],Q[i[0][1]]]
    cw_saving_sort_matrix.append(abc) 

cw_saving_sort_matrix = np.matrix(cw_saving_sort_matrix).astype(int)

loop_assign = np.zeros(len(city_list))
order_in_loop = np.zeros(len(city_list))
order_in_loop_dummy = np.zeros(len(city_list))
order_in_loop_dummy2 = np.zeros(len(city_list))

for i in range (len(cw_saving_sort)):
     
    #ikisi de boşta (1)
    if loop_assign[cw_saving_sort_matrix[i,0]] == 0 and loop_assign[cw_saving_sort_matrix[i,1]] == 0:
        r_n = max(loop_assign) + 1
        loop_assign[cw_saving_sort_matrix[i,0]] = r_n
        loop_assign[cw_saving_sort_matrix[i,1]] = r_n
#        order_in_loop[cw_saving_sort_matrix[i,0]] = 1
#        order_in_loop[cw_saving_sort_matrix[i,1]] = 2
        
        rr = 0
        for a in range(len(loop_assign)):
            if order_in_loop[a] > rr and loop_assign[a] == r_n:
                rr = order_in_loop[a]
        
        order_in_loop[cw_saving_sort_matrix[i,0]] = rr + 1
        order_in_loop[cw_saving_sort_matrix[i,1]] = rr + 2
        
        
    #ikisi de rotada (2-3-4)
    elif loop_assign[cw_saving_sort_matrix[i,0]] > 0 and loop_assign[cw_saving_sort_matrix[i,1]] > 0:
        #farklı rota
        if loop_assign[cw_saving_sort_matrix[i,0]] != loop_assign[cw_saving_sort_matrix[i,1]]:
            l_n = loop_assign[cw_saving_sort_matrix[i,0]]
            l_n2 = loop_assign[cw_saving_sort_matrix[i,1]]
            #iki loopun toplamının kapasiteyi geçip geçmediğine bak
            #------------------
            total_q_of_loop_assign = 0
            total_q_of_loop_assign2 = 0
            for y in range(len(city_list)):
                if loop_assign[y] == l_n:
                    total_q_of_loop_assign += Q[y]
                
                if loop_assign[y] == l_n2:
                    total_q_of_loop_assign2 += Q[y]
            
  
            if  total_q_of_loop_assign + total_q_of_loop_assign2 <= Vcap:
                
                #------------------
                order_in_loop_dummy = np.zeros(len(city_list))
                order_in_loop_dummy2 = np.zeros(len(city_list))
                for j in range(len(city_list)):
                    if loop_assign[j] == l_n:
                        order_in_loop_dummy[j] = order_in_loop[j]
                    else: 
                        order_in_loop_dummy[j] = 0
                
                for j in range(len(city_list)):
                    if loop_assign[j] == l_n2:
                        order_in_loop_dummy2[j] = order_in_loop[j]
                    else: 
                        order_in_loop_dummy2[j] = 0
                

                if (order_in_loop[cw_saving_sort_matrix[i,0]] == 1 or order_in_loop[cw_saving_sort_matrix[i,0]] == max(order_in_loop_dummy)) and (order_in_loop[cw_saving_sort_matrix[i,1]] == 1 or order_in_loop[cw_saving_sort_matrix[i,1]] == max(order_in_loop_dummy2)):
                    print("Yes!") 
                    print (cw_saving_sort_matrix[i,0])
                    print(cw_saving_sort_matrix[i,1])
                    kkk = np.where(loop_assign == l_n)
                    print(kkk)
                    lll = np.where(loop_assign == l_n2)
                    print(lll)  
                    alt1 = distance_matrix[0,kkk[0][0]] + distance_matrix[0,lll[0][0]] - distance_matrix[kkk[0][0],lll[0][0]]
                    print("alt1",kkk[0][0],lll[0][0],alt1)
                    alt2 = distance_matrix[0,kkk[0][0]] + distance_matrix[0,lll[0][-1]] - distance_matrix[kkk[0][0],lll[0][-1]]
                    print("alt2",kkk[0][0],lll[0][-1],alt2)
                    alt3 = distance_matrix[0,kkk[0][-1]] + distance_matrix[0,lll[0][0]] - distance_matrix[kkk[0][-1],lll[0][0]]
                    print("alt3",kkk[0][-1],lll[0][0],alt3)
                    alt4 = distance_matrix[0,kkk[0][-1]] + distance_matrix[0,lll[0][-1]] - distance_matrix[kkk[0][-1],lll[0][-1]]
                    print("alt4",kkk[0][-1],lll[0][-1],alt4)
                    
                    if max(alt1, alt2, alt3, alt4) == alt1:
                        for k in range(len(city_list)):
                            if loop_assign[k] == l_n:
                                order_in_loop[k] = max(order_in_loop_dummy) + 1 - order_in_loop_dummy[k]
                                
                            if loop_assign[k] == l_n2:
                                order_in_loop[k] = max(order_in_loop_dummy) + order_in_loop_dummy2[k]
                                loop_assign[k] = l_n 
                                
                    if max(alt1, alt2, alt3, alt4) == alt2:
                        for j in range(len(city_list)):
                            if loop_assign[j] == l_n:
                                order_in_loop[j] = max(order_in_loop_dummy2) + order_in_loop_dummy[j]
                                loop_assign[j] = l_n2
                                
                    if max(alt1, alt2, alt3, alt4) == alt3:
                        for j in range(len(city_list)):
                            if loop_assign[j] == l_n2:
                                order_in_loop[j] = max(order_in_loop_dummy) + order_in_loop_dummy2[j]
                                loop_assign[j] = l_n
                            
                    if max(alt1, alt2, alt3, alt4) == alt4:
                        for j in range(len(city_list)):
                            if loop_assign[j] == l_n2:
                                order_in_loop[j] = max(order_in_loop_dummy) + max(order_in_loop_dummy2) + 1 - order_in_loop_dummy2[j]
                                loop_assign[j] = l_n                        
   
    
    #sadece biri rotada (5-6)
    else:
        if loop_assign[cw_saving_sort_matrix[i,0]] > 0 and loop_assign[cw_saving_sort_matrix[i,1]] == 0:
            l_n = loop_assign[cw_saving_sort_matrix[i,0]]
            #atanacak olanın yüküyle mevcut loopun yükünün toplamının kapasiteyi geçip geçmediğine bak
            #---------------------------
            total_q_of_loop_assign = 0

            for z in range(len(city_list)):
                if loop_assign[z] == l_n:
                    total_q_of_loop_assign += Q[z]
            if  total_q_of_loop_assign + Q[cw_saving_sort_matrix[i,1]] <= Vcap:
                
                #---------------------------
                #sadece kendi loopunun içindeki sırasını bul
                order_in_loop_dummy = np.zeros(len(city_list))
                for j in range(len(city_list)):
                    if loop_assign[j] == l_n:
                        order_in_loop_dummy[j] = order_in_loop[j]
                    else: 
                        order_in_loop_dummy[j] = 0
                        
                if order_in_loop[cw_saving_sort_matrix[i,0]] == 1: 
                    loop_assign[cw_saving_sort_matrix[i,1]] = l_n
                    
                    for j in range(len(city_list)):
                        if loop_assign[j] == l_n:
                            order_in_loop[j] = order_in_loop[j] + 1
                            
                elif order_in_loop[cw_saving_sort_matrix[i,0]] == max(order_in_loop_dummy):
                    loop_assign[cw_saving_sort_matrix[i,1]] = l_n
                    order_in_loop[cw_saving_sort_matrix[i,1]] = max(order_in_loop_dummy) + 1
     
        elif loop_assign[cw_saving_sort_matrix[i,0]] == 0 and loop_assign[cw_saving_sort_matrix[i,1]] > 0:
            l_n = loop_assign[cw_saving_sort_matrix[i,1]]
            
            total_q_of_loop_assign = 0

            for z in range(len(city_list)):
                if loop_assign[z] == l_n:
                    total_q_of_loop_assign += Q[z]
                    
            if  total_q_of_loop_assign + Q[cw_saving_sort_matrix[i,0]] <= Vcap:
 
                #sadece kendi loopunun içindeki sırasını bul
                order_in_loop_dummy = np.zeros(len(city_list))
                for j in range(len(city_list)):
                    if loop_assign[j] == l_n:
                        order_in_loop_dummy[j] = order_in_loop[j]
                    else: 
                        order_in_loop_dummy[j] = 0
                        
                if order_in_loop[cw_saving_sort_matrix[i,1]] == 1:
                    loop_assign[cw_saving_sort_matrix[i,0]] = l_n
                    
                    for j in range(len(city_list)):
                        if loop_assign[j] == l_n:
                            order_in_loop[j] = order_in_loop[j] + 1
                            
                elif order_in_loop[cw_saving_sort_matrix[i,1]] == max(order_in_loop_dummy):
                    loop_assign[cw_saving_sort_matrix[i,0]] = l_n
                    order_in_loop[cw_saving_sort_matrix[i,0]] = max(order_in_loop_dummy) + 1
                
for i in range(no_city):
    if i > 0:
        if loop_assign[i] == 0:
            loop_assign[i] = max(loop_assign) + 1
            order_in_loop[i] = 1
              
deneme = np.transpose(np.concatenate((np.matrix(loop_assign), np.matrix(order_in_loop))))     
            

unique = np.unique(loop_assign)
unique_v1 = [i for i in unique if i!=StartCity]


index = {}
value = -1
for i in unique:
    if i != StartCity:
        value +=1
        print(np.array(np.where(deneme[:,0] == int(i)))[0,:])
        index[int(i)] = np.matrix(np.where(deneme[:,0] == int(i)))[0,:][0]

for i in range(len(unique)):
    for j in range(np.matrix(np.where(deneme[:,0] == int(unique[i])))[0,:].shape[1]):
        print(np.matrix([int(unique[i]),j+1]))
            
final_loop={}
cc = city_list[StartCity]
ii = StartCity
bb=[]
hh = []
for i in range(len(unique_v1)):
    aa=[]
    aa.append(cc)
    gg=[]
    gg.append(ii)
    
    for j in range(np.matrix(np.where(deneme[:,0] == int(unique_v1[i])))[0,:].shape[1]):
        abcde = int(np.array(np.matrix(np.where(np.logical_and(np.equal(deneme[:,0],int(unique_v1[i])),np.equal(deneme[:,1],j+1))))[0,:]))
        
        final_loop[i,j] = abcde

#        print(abcde)
        aa.append(city_list[abcde])
#        print(type(np.matrix(np.where(np.logical_and(np.equal(deneme[:,0],int(unique[i])),np.equal(deneme[:,1],j+1))))[0,:]))
        gg.append(abcde)
    aa.append(cc)
    gg.append(ii)
    print("Route",i+1, ":",*aa, sep = "-")
    bb.append(aa)  
#    print("----")
    hh.append(gg)    


 #Total_Distance_of_Routes
total_dist=[]
total_Q=[]

yuk = []
yuki = []
odoi = []
odoia = []
odoa = []
odo = []
tuketim = []
batterychange = []
sa = []
mm = 0
ma = 0

for i in range(len(unique_v1)):
     ff = 0
     pp = 0
     for j in range(np.matrix(np.where(deneme[:,0] == int(unique_v1[i])))[0,:].shape[1]):
         if j!= int(np.matrix(np.where(deneme[:,0] == int(unique_v1[i])))[0,:].shape[1])-1:
             dd = distance_matrix[final_loop[i,j],final_loop[i,j+1]]
             ff = ff + dd
             
             oo = Q[final_loop[i,j]]
             pp = pp + oo
     pp = pp + Q[final_loop[i,j]]
     ff = ff + distance_matrix[StartCity,final_loop[i,0]] + distance_matrix[final_loop[i,j], StartCity]
     print("----")
     total_dist.append(ff)
     print("Total Cost of Route -",i+1,":",total_dist[i])
     print("----")
     total_Q.append(pp)
     print("Total Load of Route -",i+1,":",total_Q[i])   
     mm = 0
     ma = 0
     my = 0
     bat = 100
     odoi = []
     odoia = []
     yuki = []
     yukig = []
     tuketimi = []
     batterychangei = []
     odoi.append(0)
     odoia.append(0)
     yuki.append(0.0)
     yukig.append(0.0)
     for f in range(len(bb[i])):
         if f > 0:
            mm += distance_matrix[bb[i][f-1]-1,bb[i][f]-1]
            ma = distance_matrix[bb[i][f-1]-1,bb[i][f]-1]
            odoi.append(mm)
            odoia.append(ma)
            
            my += Q[bb[i][f]-1]
            yuki.append(my)
            yuki[f] = float(yuki[f])
         if f < (len(bb[i]) - 1):
            yukig.append(yuki[f])
         bat -= (yukig[f]**(1/2) + 15) * odoia[f]
         batterychangei.append(bat)
    
     batterychange.append(batterychangei)
     odo.append(odoi)
     odoa.append(odoia)
     yuk.append(yukig)
     
     for f in range(len(bb[i])):
        batterylevel[i] -= (yuk[i][f]**(1/2) + 15) * odoa[i][f]
     
     
total_distance_cost = np.sum(total_dist)
print("Total Cost of All Route(s):",total_distance_cost)

total_load = np.sum(total_Q)
print("Total Load of All Route(s):",total_load)


for i in range(len(unique_v1)):
    sai=[]
    for f in range(len(bb[i])):
         sai.append(i+1)
    sa.append(sai)

key_value =[]
for i in range(len(hh)):
    for j in range(len(hh[i])):
        if j!= len(hh[i])-1:
            key_value.append((hh[i][j],hh[i][j+1]))
            

with open(r'C:\Users\Fatih\Desktop\Fatih_AYDIN_END507_Proje\batchange.csv', 'w',newline="") as csvfile:
    cwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cwriter.writerow('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    for i in range(len(unique_v1)):
        cwriter.writerow(batterychange[i])


with open(r'C:\Users\Fatih\Desktop\Fatih_AYDIN_END507_Proje\route.csv', 'w',newline="") as csvfile:
    cwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cwriter.writerow('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    for i in range(len(unique_v1)):
        cwriter.writerow(bb[i])


with open(r'C:\Users\Fatih\Desktop\Fatih_AYDIN_END507_Proje\loopnr.csv', 'w',newline="") as csvfile:
    cwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cwriter.writerow('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    for i in range(len(unique_v1)):
        cwriter.writerow(sa[i])