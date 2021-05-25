import matplotlib.pyplot as plt

x0 = []
y0 = []
y1 = []

for line in open('log.txt', 'r'):
    lines = [i for i in line.split()]
    x0.append(lines[0])
    y0.append(float(lines[1]))
    y1.append(float(lines[2]))

plt.title("Students Marks")
plt.xlabel('Roll Number')
plt.ylabel('Marks')
plt.yticks(y0)
plt.yticks(y1)
plt.plot(x0, y0, marker = 'o', c = 'g')
plt.plot(x0, y1, marker = 'o', c = 'r')

plt.show()
