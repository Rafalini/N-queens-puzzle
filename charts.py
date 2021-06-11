import matplotlib.pyplot as plt
import sys
import random

n = len(sys.argv)
if(n<2):
    print("no file name provided!")

allHeaders = []
data = []

plt.title("Alghoritm efficiency\n")
plt.xlabel('Epochs')
plt.ylabel('Fitness')
for arg in sys.argv[1:]:
    with open(arg, 'r') as f:
        headers = [i for i in  f.readline().split(",")]
        headers[len(headers)-1] = headers[len(headers)-1][0:-2] #slice endline
        allHeaders += headers

        offset = len(data)
        for h in headers:
            data.append([])
        for line in f:
            fields = [i for i in line.split(",")]
            for i in range(len(fields)):
                data[offset+i].append(float(fields[i]))

min = 0                 #unify data lenght
for dat in data:
    if min < len(dat):
        min = len(dat)
for dat in data:
    dat = dat[:min]

for i in range(len(sys.argv)-1):
    offset = i * 3
    # plt.plot(data[0], data[i], label=allHeaders[i])
    # plt.plot(data[0], data[offset+1], label=allHeaders[offset+1])
    plt.plot(data[0], data[offset+2], label=allHeaders[offset+2])

plt.legend()
plt.show()
