##############################################################################
##  Zachar Hankewycz, 2018                                                  ##
##  If you plan on editing this, may God have mercy on your soul            ##
##  This could could be the basis for a book called "Poor Python Practices" ##
##############################################################################

import decimal
import pyperclip
import datetime
import math
from colorama import init
init()
# Initial user information
from colorama import Fore, Back, Style
print(Fore.WHITE + Style.BRIGHT + '\n\n***********************************' + Style.RESET_ALL)
print(Fore.RED + Style.BRIGHT + 'All measurments are in millimeters.\nAll output is saved to backupModel.bak' + Style.RESET_ALL)
print(Fore.WHITE + Style.BRIGHT + '***********************************\n' + Style.RESET_ALL)

# General web structure input (Overall radius)
while True:
    try:
        webRadius = decimal.Decimal(input("Radius of the web structure (max radius): "))
        while webRadius <= 1:
            print("Invalid input, please try again (must be a positive rational number)")
            webRadius = decimal.Decimal(input("Radius of the web structure (max radius): "))
        break
    except:
            print("Invalid input, please try again (must be a positive rational number)")
    
# Radial thread input (Quantity and radius)
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

# Spiral thread input (Quantity, radius, and spacing)
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

# Initializes the output by defining the number of fragments (quality of the model. Lower is faster, higher is more defined)
initial = "$fn=30;\n"

# Creating/adding the radial threads to initial
initialDegrees = round((360 / radialQuantity), 2)
a = 0
degrees = 0
while a < radialQuantity:
        initial += str("rotate([90,0," + str(degrees) +"])translate([0, 0, -" + str(webRadius) + "])linear_extrude(height = " + str(webRadius) + ")circle(r = " + str(radialRadius) + ");\n")
        a += 1
        degrees += initialDegrees

# Spiral threads
b = 0
# Degrees calculations (used later to find triangle side lengths)
sideAngleDegrees = (180 - initialDegrees) / 2
halfMainAngleDegrees = round((initialDegrees / 2), 4)
# Used to determine the next spiral length
spiralDistance2 = initialSpiralDistance
initialSpiralDistance2 = initialSpiralDistance
# Determines how much each spiral thread must increase by to reach the desired spiral

# Could be done as an if statement
spiralDistanceIncrement = spiralDistance / radialQuantity


spiralDiagonal = 0

# Defines initial degree rotation angle
degrees = decimal.Decimal(math.fabs((90 - halfMainAngleDegrees) - initialDegrees)) # Used to get rotation angle
degrees = (90 - halfMainAngleDegrees)
while degrees > initialDegrees:
    degrees = degrees - initialDegrees
initialDegreesRotation = degrees


spiralDistanceFinal = (spiralDistance + (spiralDistance / radialQuantity) / 2)
q = 0
w = 0 
d = 0

spiralIncrement = 0
while b < spiralQuantity and spiralDistance < webRadius and spiralDiagonal < webRadius:
    # Determine length of the spiral thread
    spiralLength = round((((spiralDistance) * decimal.Decimal(math.sin(math.radians(halfMainAngleDegrees))))/decimal.Decimal(math.sin(math.radians(sideAngleDegrees)))) * 2, 4)
    
    if q == 0:
        spiralTranslate = (spiralLength / -2)
        # q is incremented later on, no need to do it here
        spiralLengthInitial = spiralLength
        previousSpiralLength = spiralLength
        spiralDiagonal = decimal.Decimal(math.sqrt(((spiralLength / 2) ** 2 + spiralDistance ** 2)))

    
    # defining arbitrary variables used only for incrementing
    # this is a terrible solution and there's got to be a much better way
    k = 0
    x = 0
    r = 1
    while k < radialQuantity:
        if r == 1:
            if spiralSpacingType == "f":
                spiralDistance2 += initialSpiralDistance
            elif spiralSpacingType == "l":
                if d != 0:
                    initialSpiralDistance2 += spiralLinearConstant
                spiralDistance2 += initialSpiralDistance2
                d += 1
            elif spiralSpacingType == "g":
                spiralDistance2 += initialSpiralDistance
                spiralDistance2 *= spiralGeometricConstant
                
            spiralLength2 = round(((spiralDistance2 * decimal.Decimal(math.sin(math.radians(halfMainAngleDegrees))))/decimal.Decimal(math.sin(math.radians(sideAngleDegrees)))) * 2, 4)
        
            spiralDiagonalNextLevel = decimal.Decimal(math.sqrt(((spiralLength2 / 2) ** 2) + spiralDistance2 ** 2))

            try:
                previousSpiralDiagonalNextLevel
            except NameError:
                spiralIncrement = (spiralDiagonalNextLevel - spiralDiagonal) / radialQuantity
            else:
                spiralIncrement = (spiralDiagonalNextLevel - previousSpiralDiagonalNextLevel) / radialQuantity

            previousSpiralDiagonalNextLevel = spiralDiagonalNextLevel

        spiralDiagonal2 = decimal.Decimal(spiralDiagonal) + spiralIncrement


        spiralLength = round(math.sqrt(decimal.Decimal(spiralDiagonal ** 2) + spiralDiagonal2 ** 2 - (2 * spiralDiagonal * spiralDiagonal2 * decimal.Decimal(math.cos(math.radians(initialDegrees))))), 4)
        
        # VERY hacky solution. Ignore for now. Traffic fines double in work zones.

        if q == 0:
            spiralTranslate += 1 - (decimal.Decimal(spiralLength) - spiralLengthInitial) / 2
            q += 1
            if initialSpiralDistance > 6:
                spiralTranslate += decimal.Decimal(0.66) * (decimal.Decimal(initialSpiralDistance / 4) - 1)
            if radialQuantity > 12:
                spiralTranslate -= decimal.Decimal(0.35)
            elif radialQuantity > 9:
                spiralTranslate -= decimal.Decimal(0.3)
            elif radialQuantity > 7:
                spiralTranslate -= decimal.Decimal(0.1)
            elif radialQuantity > 5:
                spiralTranslate -= decimal.Decimal(0.15)

        else:
            spiralTranslate -= ((decimal.Decimal(spiralLength)-decimal.Decimal(previousSpiralLength)) / 2)
        spiralTranslate = round(spiralTranslate, 4)   
        
        # End hacky solution zone. 
        

        largeSideDegree = math.asin(decimal.Decimal(math.sin(math.radians(initialDegrees))) * decimal.Decimal(spiralDiagonal2) / decimal.Decimal(spiralLength))
        largeSideDegree = round(decimal.Decimal(math.degrees(largeSideDegree)), 4)
        
        if degrees <= 360:
            if w == 0:

                degrees = degrees - initialDegreesRotation + largeSideDegree
                w += 1
            else:
                degrees = largeSideDegree - (initialDegrees * w)
                w += 1

            #if x % 2 == 0:
            ############print(spiralDistanceFinal)

            initial += str("rotate([90,0," + str(degrees) +"])translate([" + str(spiralDistanceFinal) + ", 0, " + str(spiralTranslate) + "])linear_extrude(height = " + str(spiralLength) + ")circle(r = " + str(spiralRadius) + ");\n")

            print(spiralDistanceFinal)
            # Changes spiralDistance counting to be compatible w/ linear and geometric
            if r == radialQuantity and spiralSpacingType == "l":
                spiralDistanceFinal += spiralDistanceIncrement / 2
            elif r == radialQuantity and spiralSpacingType == "g":
                spiralDistanceFinal += spiralDistanceIncrement / 2
            else:
                spiralDistanceFinal += spiralDistanceIncrement
            r += 1

            


            #spiralDistanceIncrement = spiralDistance / radialQuantity

            previousSpiralLength = spiralLength
            x += 1
        
        # degrees = (90 - halfMainAngleDegrees) - initialDegrees
        spiralDiagonal = spiralDiagonal2

        k += 1

    if spiralSpacingType == "l":
        spiralDistanceIncrement += spiralLinearConstant / radialQuantity
        spiralDistanceFinal += spiralDistanceIncrement / 2

    elif spiralSpacingType == "g":
        spiralDistanceIncrement *= spiralGeometricConstant
        spiralDistanceFinal += spiralDistanceIncrement / 2
   



    b += 1  
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