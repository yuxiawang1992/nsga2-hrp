
import os

path = "D:\\PythonCode\\NSGA-II\\result\\txt\\pareto_front\\"

gmin = 10
for file in os.listdir(path):
    f = open(path+file,'r')
    lines = f.readlines()
    chro = file.split('-')[0]
    min = 5
    if chro == '15':
        for i in range(1,len(lines)):
            dis = float(lines[i].split(',')[2]) + float(lines[i].split(',')[1])
            if dis <= min:
                min = dis
        print(chro + " --- " + file.split('-')[1] + " --- " + str(min))

    if min <= gmin:
        gmin = min

print(" minimized is ------ "+ str(gmin))