from colorama import init
import colorama
from colorama import Fore, Back, Style
import random
init() #colorama init

f = open("test.txt", "r+")
x = ''
data = f.read()
for i in data.split():
	x = x + i + " . "

colors = list(vars(colorama.Fore).values())
colored_chars = [random.choice(colors) + char for char in x.split(" .")]
print(''.join(colored_chars))
f.close()