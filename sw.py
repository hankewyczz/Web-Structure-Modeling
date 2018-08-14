import decimal
import pyperclip
import datetime
import math
from colorama import init
init()

# Initial user information
from colorama import Fore, Back, Style
print(Fore.RED + Style.DIM + Back.WHITE + 'All measurments are in millimeters.\nAll output is saved to backupModel.bak\n')
print(Style.RESET_ALL)

# General web structure input
while True:
    try:
        webRadius = decimal.Decimal(input("Radius of the web structure (max radius): "))
        while webRadius <= 1:
            print("Invalid input, please try again (must be a positive rational number)")
            webRadius = decimal.Decimal(input("Radius of the web structure (max radius): "))
        break
    except:
            print("Invalid input, please try again (must be a positive rational number)")
    
# Radial thread input
while True:
    try:
        radialQuantity = decimal.Decimal(input("Number of radial threads: "))
        while radialQuantity <  0:
            print("Invalid input, please try again (must be a positive rational number)")
            radialQuantity = decimal.Decimal(input("Number of radial threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")
while True:
    try:
        radialRadius = decimal.Decimal(input("Radius of radial threads: "))
        while radialRadius <=  0:
            print("Invalid input, please try again (must be a positive rational number)")
            radialRadius = decimal.Decimal(input("Radius of radial threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")

# Spiral thread input
while True:
    try:
        spiralQuantity = decimal.Decimal(input("Desired number of spiral threads: "))
        while spiralQuantity < 0:
            print("Invalid input, please try again (must be a positive rational number)")
            spiralQuantity = decimal.Decimal(input("Desired number of spiral threads: "))
        break
    except:
        prdecimal.Decimal("Invalid input, please try again (must be a positive rational number)")
while True:
    try:
        spiralRadius = decimal.Decimal(input("Desired radius of spiral threads: "))
        while spiralRadius <= 0:
            print("Invalid input, please try again (must be a positive rational number)")
            spiralRadius = decimal.Decimal(input("Desired radius of spiral threads: "))
        break
    except:
        print("Invalid input, please try again (must be a positive rational number)")
while True:
    try:
        initialSpiralDistance = decimal.Decimal(input("Base distance between spiral threads: "))
        while initialSpiralDistance <= 0:
            print("Invalid input, please try again (must be a positive rational number)")
            initialSpiralDistance = decimal.Decimal(input("Base distance between spiral threads: "))
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
            spiralLinearConstant = decimal.Decimal(input("Linear constant (by what constant will the distance linearly increase?: "))
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
degreesInitial = round((360 / radialQuantity), 2)

j = 0
degrees = 0
while j < radialQuantity:
        initial += str("rotate([90,0," + str(degrees) +"])translate([0, 0, -" + str(webRadius) + "])linear_extrude(height = " + str(webRadius) + ")circle(r = " + str(radialRadius) + ");\n")
        j += 1
        degrees += degreesInitial

# Spiral threads
i = 0
# Degrees calculations (used later to find triangle side lengths)
spiralRotateDegrees = round((degreesInitial / 2), 2)
sideDegrees = (180 - degreesInitial) / 2
sideDegreesRad = math.radians(sideDegrees)
mainDegrees = degreesInitial / 2
mainDegreesRad = math.radians(mainDegrees)
spiralDiagonal = 0
degrees = (90 - spiralRotateDegrees) - degreesInitial # Used to get rotation angle

while degrees > degreesInitial:
    degrees = degrees - degreesInitial
## Not necessary rn- bounding circle ## initial += str("color([0,0,0]) rotate_extrude()translate([" + str(webRadius) + ",0,0])circle(r=1);\n")
while i < spiralQuantity and spiralDistance < webRadius and spiralDiagonal < webRadius:
    # Determine length of the spiral thread
    spiralLength = round(((spiralDistance * decimal.Decimal(math.sin(mainDegreesRad)))/decimal.Decimal(math.sin(sideDegreesRad))) * 2, 4)
    spiralTranslate = (spiralLength / -2)
    spiralDiagonal = math.sqrt(((spiralLength / 2) ** 2 + spiralDistance ** 2))

    while degrees <= 360:
        initial += str("rotate([90,0," + str(degrees) +"])translate([" + str(spiralDistance) + ", 0, " + str(spiralTranslate) + "])linear_extrude(height = " + str(spiralLength) + ")circle(r = " + str(spiralRadius) + ");\n")
        degrees += degreesInitial
    degrees = (90 - spiralRotateDegrees) - degreesInitial
    while degrees > degreesInitial:
        degrees = degrees - degreesInitial
    i += 1  
    if spiralSpacingType == "f":
        spiralDistance += initialSpiralDistance
    elif spiralSpacingType == "l":
        initialSpiralDistance += spiralLinearConstant
        spiralDistance += initialSpiralDistance
    elif spiralSpacingType == "g":
        spiralDistance += initialSpiralDistance
        spiralDistance *= spiralGeometricConstant


# File save + clipboard copy
pyperclip.copy(initial)
file = open("backupModel.bak", "a+")
file.write("\n\n\n\n" + str(datetime.datetime.now()) + "\n")
file.write(initial)
file.close()

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