radNumber = int(input("Number of radial threads: "))
radRadius = input("Radius of radial threads: ")

initial = "$fa=.5; $fs=0.5; $fn=100;\n"
degreesInitial = 180 / radNumber
degreesSTR = str(degreesInitial)

j = 0
while j < radNumber:
		initial += str("rotate([90,0," + degreesSTR +"])translate([0, 0, -250])linear_extrude(height = 500)circle(r = " + radRadius + ");\n")
		j += 1
		degrees = degreesInitial + degreesInitial * j
		degreesSTR = str(degrees)

print(initial)