import decimal
import pyperclip
import datetime
import math
from colorama import init
init()

from colorama import Fore, Back, Style
print(Fore.RED + Style.DIM + Back.WHITE + 'All measurments are in millimeters.\nAll output is saved to backupModel.bak\n')
print(Style.RESET_ALL)

# General web
while True:
    try:
        webRadius = int(input("Radius of the web structure (max radius): "))
        webRadiusStr = str(webRadius)
        while webRadius <= 1:
            print("Invalid input, please try again (must be a positive rational number)")
            webRadius = int(input("Radius of the web structure (max radius): "))
        break
    except:
            print("Invalid input, please try again (must be a positive rational number)")
    
# Radial threads
while True:
    try:
        radialQuantity = int(input("Number of radial threads: "))
        while radialQuantity <  0:
            print("Invalid input, please try again (must be a positive rational number)")
            radialQuantity = int(input("Number of radial threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")
while True:
    try:
        radialRadius = int(input("Radius of radial threads: "))
        while radialRadius <=  0:
            print("Invalid input, please try again (must be a positive rational number)")
            radialRadius = int(input("Radius of radial threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")

# Spiral threads
while True:
    try:
        spiralQuantity = int(input("Desired number of spiral threads: "))
        while spiralQuantity < 0:
            print("Invalid input, please try again (must be a positive rational number)")
            spiralQuantity = int(input("Desired number of spiral threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")
while True:
    try:
        spiralRadius = int(input("Desired radius of spiral threads: "))
        while spiralRadius <= 0:
            print("Invalid input, please try again (must be a positive rational number)")
            spiralRadius = int(input("Desired radius of spiral threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")
while True:
    try:
        initialSpiralDistance = int(input("Base distance between spiral threads: "))
        while initialSpiralDistance <= 0:
            print("Invalid input, please try again (must be a positive rational number)")
            initialSpiralDistance = int(input("Base distance between spiral threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")
spiralDistance = initialSpiralDistance

# Spacing types
spiralSpacingType = input("Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ")
while spiralSpacingType != "f" and spiralSpacingType != "l" and spiralSpacingType != "g":
    print("Invalid response.")
    spiralSpacingType = input("Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ")

# Spacing type-specific questions
if spiralSpacingType == "l":
    while True:
        try:
            spiralLinearConstant = int(input("Linear constant (by what constant will the distance linearly increase?: "))
            while spiralLinearConstant < 0:
                print("Invalid input, please try again (must be a positive rational number)")
                spiralLinearConstant = int(input("Linear constant (by what constant will the distance linearly increase?: "))
            break
        except:
            print("Invalid input, please try again (must be a positive rational number)")
elif spiralSpacingType == "g":
    while True:
        try:
            spiralGeometricConstant = decimal.Decimal(input("Geometric ratio: "))
            while spiralGeometricConstant <= 0:
                print("Invalid input, please try again (must be a positive rational number)")
                spiralGeometricConstant = decimal.Decimal(input("Geometric ratio:" ))
            break
        except:
            print("Invalid input, please try again (must be a positive rational number)")

initial = "$fn=30;\n"
# Radial Threads
degreesInitial = 360 / radialQuantity
sideDegrees = (180 - degreesInitial) / 2
sideDegreesRad = math.radians(sideDegrees)
mainDegrees = degreesInitial / 2
mainDegreesRad = math.radians(mainDegrees)
degreesSTR = str(degreesInitial)
j = 0
while j < radialQuantity:
        initial += str("rotate([90,0," + degreesSTR +"])translate([0, 0, -" + webRadiusStr + "])linear_extrude(height = " + webRadiusStr + ")circle(r = " + str(radialRadius) + ");\n")
        j += 1
        degrees = degreesInitial + degreesInitial * j
        degreesSTR = str(degrees)


i = 0
while i < spiralQuantity and spiralDistance < webRadius:
    initial += str("rotate_extrude()translate([" + str(spiralDistance) + ",0,0])circle(r=" + str(spiralRadius) + ");\n")

    i += 1  
    if spiralSpacingType == "f":
        spiralDistance += initialSpiralDistance
    elif spiralSpacingType == "l":
        initialSpiralDistance += spiralLinearConstant
        spiralDistance += initialSpiralDistance
    elif spiralSpacingType == "g":
        spiralDistance += initialSpiralDistance
        spiralDistance *= spiralGeometricConstant



# Additional info
saveas = input("Would you like to save your output as a .scad file? (y/n): ")
if saveas == "y" or saveas == "Y":
    saveas_name = input("What would you like to save your output as? (filename): ")
    if ".scad" not in saveas_name:
        saveas_name += ".scad"
        print(saveas_name)
    file_saveas = open(saveas_name, "w+")
    file_saveas.write(initial)
    file_saveas.close()

# File save + clipboard copy
pyperclip.copy(initial)
file = open("backupModel.bak", "a+")
file.write("\n\n\n\n" + str(datetime.datetime.now()) + "\n")
file.write(initial)
file.close()