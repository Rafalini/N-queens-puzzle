import matplotlib.pyplot as plt
import sys

n = len(sys.argv)
if(n<2):
    print("no file name provided!")

headers = []
data = [[]]
algName = sys.argv[1][4:]

plt.title("Alghoritm efficiency \n"+algName)
plt.xlabel('Epochs')
plt.ylabel('Fitness')

with open(sys.argv[1], 'r') as f:
    headers = [i for i in  f.readline().split(",")]
    headers[len(headers)-1] = headers[len(headers)-1][0:-2] #slice endline

    for h in headers:
        data.append([])

    for line in f:
        fields = [i for i in line.split(",")]

        for i in range(len(fields)):
            if i == 0:
                data[i].append(fields[i])
            else:
                data[i].append(float(fields[i]))

# plt.yticks(data[1])
# plt.yticks(data[2])
plt.plot(data[0], data[1], c = 'g', label=headers[1])
plt.plot(data[0], data[2], c = 'r', label=headers[2])
plt.legend()
plt.show()
