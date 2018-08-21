##############################################################################
##  Zachar Hankewycz, 2018                                                  ##
##  If you plan on editing this, may God have mercy on your soul            ##
##  This could could be the basis for a book called "Poor Python Practices" ##
##############################################################################

from decimal import Decimal as dec
import random
from random import randint
import pyperclip
import datetime
import math
from math import sin as sin
from math import radians as rad
import time
from colorama import init
init()
# Initial user information
from colorama import Fore, Back, Style
print(Fore.WHITE + Style.BRIGHT + '\n\n***********************************' + Style.RESET_ALL)
print(Fore.RED + Style.BRIGHT + 'All measurments are in millimeters.\nAll output is saved to backupModel.bak' + Style.RESET_ALL)
print(Fore.WHITE + Style.BRIGHT + '***********************************\n' + Style.RESET_ALL)

# For user customizability, set quickTest to anything but "enabled" or "random"
quickTest = "enabledNOT"
if quickTest == "enabled":
    webRadius = dec(20)
    radialQuantity = dec(5)
    radialRadius = round(dec(.1), 1)
    spiralQuantity = dec(2)
    spiralRadius = round(dec(.1), 1)
    initialSpiralDistance = round(dec(4), 1)
    spiralSpacingType = "g"
    spiralLinearConstant = round(dec(4), 1)
    spiralGeometricConstant = round(dec(1.1), 2)

elif quickTest == "random":
    webRadius = dec(randint(20, 100))
    radialQuantity = dec(randint(2, 30))
    radialRadius = dec(random.random())
    spiralQuantity = dec(randint(1, 100))
    spiralRadius = radialRadius
    initialSpiralDistance = dec(randint(1, 20))
    spiralSpacingType = "g"
    spiralLinearConstant = dec(randint(1, 15))
    spiralGeometricConstant = dec(random.random() + randint(0,1))
else:
    # General web structure input (Overall radius)
    while True:
        try:
            webRadius = dec(input("Radius of the web structure (max radius): "))
            while webRadius <= 1:
                print("Invalid input, please try again (must be a positive rational number)")
                webRadius = dec(input("Radius of the web structure (max radius): "))
            break
        except:
                print("Invalid input, please try again (must be a positive rational number)")
        
    # Radial thread input (Quantity and radius)
    while True:
        try:
            radialQuantity = dec(input("Number of radial threads: "))
            while radialQuantity <  0:
                print("Invalid input, please try again (must be a positive rational number)")
                radialQuantity = dec(input("Number of radial threads: "))
            break
        except:
            print("Invalid input, please try again (must be a positive rational number)")
    while True:
        try:
            radialRadius = dec(input("Radius of radial threads: "))
            while radialRadius <=  0:
                print("Invalid input, please try again (must be a positive rational number)")
                radialRadius = dec(input("Radius of radial threads: "))
            break
        except:
            print("Invalid input, please try again (must be a positive rational number)")

    # Spiral thread input (Quantity, radius, and spacing)
    while True:
        try:
            spiralQuantity = dec(input("Desired number of spiral threads: "))
            while spiralQuantity < 0:
                print("Invalid input, please try again (must be a positive rational number)")
                spiralQuantity = dec(input("Desired number of spiral threads: "))
            break
        except:
            prdec("Invalid input, please try again (must be a positive rational number)")
    while True:
        try:
            spiralRadius = dec(input("Desired radius of spiral threads: "))
            while spiralRadius <= 0:
                print("Invalid input, please try again (must be a positive rational number)")
                spiralRadius = dec(input("Desired radius of spiral threads: "))
            break
        except:
            print("Invalid input, please try again (must be a positive rational number)")
    while True:
        try:
            initialSpiralDistance = dec(input("Base distance between spiral threads: "))
            while initialSpiralDistance <= 0:
                print("Invalid input, please try again (must be a positive rational number)")
                initialSpiralDistance = dec(input("Base distance between spiral threads: "))
            break
        except:
            print("Invalid input, please try again (must be a positive rational number)")
    

    # Spacing types
    spiralSpacingType = input("Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ")
    while spiralSpacingType != "f" and spiralSpacingType != "l" and spiralSpacingType != "g":
        print("Invalid response.")
        spiralSpacingType = input("Is the spiral thread spacing fixed, linear, or geometric? (Respond f, l, or g): ")

    # Spacing type-specific questions
    if spiralSpacingType == "l":
        while True:
            try:
                spiralLinearConstant = dec(input("Linear constant (by what constant will the distance linearly increase?: "))
                break
            except:
                print("Invalid input, please try again (must be a positive rational number)")
    elif spiralSpacingType == "g":
        while True:
            try:
                spiralGeometricConstant = dec(input("Geometric ratio: "))
                while spiralGeometricConstant <= 0:
                    print("Invalid input, please try again (must be a positive rational number)")
                    spiralGeometricConstant = dec(input("Geometric ratio:" ))
                break
            except:
                print("Invalid input, please try again (must be a positive rational number)")
spiralDistance = initialSpiralDistance
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
degrees = dec(math.fabs((90 - halfMainAngleDegrees) - initialDegrees)) # Used to get rotation angle
degrees = (90 - halfMainAngleDegrees)
while degrees > initialDegrees:
    degrees = degrees - initialDegrees
initialDegreesRotation = degrees


spiralDistanceOriginal = (spiralDistance + (spiralDistance / radialQuantity) / 2)
q = 0
w = 0 
d = 0

spiralIncrement = 0
while b < spiralQuantity and spiralDistance < webRadius and spiralDiagonal < webRadius:
    # Determine length of the spiral thread
    spiralLength = round((((spiralDistance) * dec(sin(rad(halfMainAngleDegrees))))/dec(sin(rad(sideAngleDegrees)))) * 2, 4)
    
    if q == 0:
        spiralTranslate = (spiralLength / -2)
        q += 1
        spiralLengthInitial = spiralLength
        previousSpiralLength = spiralLength
        spiralDiagonal = round(dec(math.sqrt(((spiralLength / 2) ** 2 + spiralDistance ** 2))), 4)

    
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
                
            spiralLength2 = round(((spiralDistance2 * dec(sin(rad(halfMainAngleDegrees))))/dec(sin(rad(sideAngleDegrees)))) * 2, 4)
        
            spiralDiagonalNextLevel = dec(math.sqrt(((spiralLength2 / 2) ** 2) + spiralDistance2 ** 2))

            try:
                previousSpiralDiagonalNextLevel
            except NameError:
                spiralIncrement = (spiralDiagonalNextLevel - spiralDiagonal) / radialQuantity
            else:
                spiralIncrement = (spiralDiagonalNextLevel - previousSpiralDiagonalNextLevel) / radialQuantity


            previousSpiralDiagonalNextLevel = spiralDiagonalNextLevel

        spiralDiagonal2 = round(dec(spiralDiagonal) + spiralIncrement, 4)


        spiralLength = round(dec(math.sqrt(dec(spiralDiagonal ** 2) + spiralDiagonal2 ** 2 - (2 * spiralDiagonal * spiralDiagonal2 * dec(math.cos(rad(initialDegrees)))))), 4)

        

        largeSideDegree = math.asin(dec(sin(rad(initialDegrees))) * dec(spiralDiagonal2) / dec(spiralLength))
        largeSideDegree = round(dec(math.degrees(largeSideDegree)), 4)

        if degrees <= 360:
            if w == 0:
                degrees = degrees - initialDegreesRotation + largeSideDegree
                while degrees < 0:
                    degrees += 360
                w += 1
            else:
                degrees = largeSideDegree - (initialDegrees * w)
                while degrees < 0:
                    degrees += 360
                w += 1


            spiralDistanceFinal = dec(round(spiralDiagonal * dec(sin(rad(largeSideDegree))), 4))

            degreeDifference = degrees - initialDegreesRotation
            while degreeDifference > halfMainAngleDegrees:
                degreeDifference -= halfMainAngleDegrees

           
            spiralLengthOriginal = 2 * round((spiralDistanceFinal*dec(sin(rad(halfMainAngleDegrees))))/dec(sin(rad(sideAngleDegrees))), 4)
            spiralLengthOriginalSegment = (dec(sin(rad(halfMainAngleDegrees-degreeDifference/2)))*spiralDistanceFinal)/dec(sin(rad(sideAngleDegrees)))

            spiralTranslateInitialDifference = round(dec(math.sqrt(spiralDistanceFinal ** 2 + spiralDistanceOriginal ** 2 - 2*spiralDistanceFinal*spiralDistanceOriginal*dec(math.cos(rad(degreeDifference))))), 4)
            spiralTranslate3rdDegree = 90 - degreeDifference
            spiralDistanceOriginalShortened = spiralDistanceFinal / dec(sin(rad(spiralTranslate3rdDegree)))
            
            if spiralSpacingType == "g":
                spiralTranslate2ndDifference = dec(math.sqrt((2 * spiralDistanceFinal ** 2) - 2*spiralDistanceFinal*spiralDistanceFinal*dec(math.cos(rad(degreeDifference)))))
                spiralTranslate3rdDifference = dec((spiralDistanceOriginalShortened * dec(sin(rad(sideAngleDegrees)))) / dec(sin(rad(180 - sideAngleDegrees - degreeDifference))))
                spiralTranslate3rdDifference = spiralTranslate3rdDifference - spiralDistanceOriginalShortened
                spiralTranslate2 = round(spiralTranslate2ndDifference - spiralTranslate3rdDifference, 4)
            else:
                spiralTranslate2ndDifference = (spiralDistanceFinal * dec(sin(rad(degreeDifference))) / dec(sin(rad(spiralTranslate3rdDegree))))
                spiralTranslate3rdDifference = (spiralDistanceOriginal - spiralDistanceOriginalShortened) / dec(sin(rad(degreeDifference)))
                spiralTranslate2 = round(spiralTranslate2ndDifference + spiralTranslate3rdDifference, 4)  


             
            spiralTranslate2 -= round(dec(spiralLength) / 2, 4)



            initial += str("rotate([90,0," + str(degrees) +"])translate([" + str(spiralDistanceFinal) + ", 0, " + str(spiralTranslate2) + "])linear_extrude(height = " + str(spiralLength) + ")circle(r = " + str(spiralRadius) + ");\n")

            # Changes spiralDistance counting to be compatible w/ linear and geometric


            if r == radialQuantity and spiralSpacingType == "l":
                spiralDistanceOriginal += spiralDistanceIncrement / 2
            elif r == radialQuantity and spiralSpacingType == "g":
                spiralDistanceOriginal += spiralDistanceIncrement / 2
            else:
                spiralDistanceOriginal += spiralDistanceIncrement
            r += 1

            


            #spiralDistanceIncrement = spiralDistance / radialQuantity

            previousSpiralLength = spiralLength
            x += 1
        
        # degrees = (90 - halfMainAngleDegrees) - initialDegrees
        spiralDiagonal = spiralDiagonal2

        k += 1
 
    if spiralSpacingType == "l":
        spiralDistanceIncrement += spiralLinearConstant / radialQuantity
        spiralDistanceOriginal += spiralDistanceIncrement / 2

    elif spiralSpacingType == "g":
        spiralDistanceIncrement *= spiralGeometricConstant
        spiralDistanceOriginal += spiralDistanceIncrement / 2





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
## FIN ##