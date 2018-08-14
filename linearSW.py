spiThread = int(input("Desired number of spiral threads: "))
spiWidth = int(input("Desired radius of spiral threads: "))
initialDistance = int(input("Distance from center to the first spiral thread: "))
spiDistanceOriginal = int(input("Desired distance between spiral threads (constant): "))

initial = "$fa=.5; $fs=0.5; $fn=100;\n"
spiDistance = spiDistanceOriginal + initialDistance

i = 0
while i < spiThread:
	if i < 1:
		initial += str("rotate_extrude()translate([" + str(initialDistance) + ",0,0])circle(r=" + str(spiWidth) + ");\n")
		i += 1
	else:
		initial += str("rotate_extrude()translate([" + str(spiDistance) + ",0,0])circle(r=" + str(spiWidth) + ");\n")
		i += 1	
		spiDistance += spiDistanceOriginal

print(initial)
