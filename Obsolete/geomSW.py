import decimal

spiThread = int(input("Desired number of spiral threads: "))
spiWidth = int(input("Desired radius of spiral threads: "))
initialDistance = int(input("Distance from center to the first spiral thread: "))
spiDistanceOriginal = decimal.Decimal(input("Desired distance between spiral threads (geometric): "))
radNumber = int(input("Number of radial threads: "))
radRadius = input("Radius of radial threads: ")

initial = "$fa=.5; $fs=0.5; $fn=100;\n"
spiDistance = spiDistanceOriginal * initialDistance

degreesInitial = 180 / radNumber
degreesSTR = str(degreesInitial)

i = 0
while i < spiThread:
	if i < 1:
		initial += str("rotate_extrude()translate([" + str(initialDistance) + ",0,0])circle(r=" + str(spiWidth) + ");\n")
		i += 1
	else:
		initial += str("rotate_extrude()translate([" + str(spiDistance) + ",0,0])circle(r=" + str(spiWidth) + ");\n")
		i += 1	
		spiDistance = round(spiDistanceOriginal * spiDistance, 2)

j = 0
while j < radNumber:
		initial += str("rotate([90,0," + degreesSTR +"])translate([0, 0, -250])linear_extrude(height = 500)circle(r = " + radRadius + ");\n")
		j += 1
		degrees = degreesInitial + degreesInitial * j
		degreesSTR = str(degrees)
		
print(initial)
