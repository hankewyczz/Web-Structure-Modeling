from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import pyperclip
from decimal import Decimal as dec

f = open('C:/Users/Zachar/Documents/MATLAB/matlab.xyz', 'r')

lines = f.readlines()
lines = lines[2:]
words = '   '.join([line.strip() for line in lines])
words = words.replace("   1   ", "   ")
words = words.replace("   2   ", "   ")
words = words.replace("   3   ", "   ")
words = words[4:]

a = words.split("   ")
x = a
y = a
z = a

x = [v for i, v in enumerate(x) if i % 3 == 0]
y = [v for i, v in enumerate(y) if i % 3 == 1]
z = [v for i, v in enumerate(z) if i % 3 == 2]


# This is a really bad way of doing this, but whatever 
x = str(x)
y = str(y)
z = str(z)
x = x.replace("', '", " ")
x = x.replace("'", "")
x = x.replace("[", "")
x = x.replace("]", "")
y = y.replace("', '", " ")
y = y.replace("'", "")
y = y.replace("[", "")
y = y.replace("]", "")
z = z.replace("', '", " ")
z = z.replace("'", "")
z = z.replace("[", "")
z = z.replace("]", "")
x = x.split()
y = y.split()
z = z.split()


x = [float(i) for i in x]
y = [float(i) for i in y]
z = [float(i) for i in z]


fig = plt.figure()

ax = fig.gca(projection='3d')
ax.scatter(x, y, z)
plt.show()