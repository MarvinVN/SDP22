from gpiozero import Button
import sys



# defining pin numbers
p1_hit_button = Button(17)
p1_stand_button = Button(27)
p1_double_button = Button(22)
p1_exit_button = Button(23)	

#testing button functionality
while(1):
	if p1_hit_button.is_pressed:
		#want to update the gui that event was detected; SLOT to eventDetected()
		print("P1 Hit Button was pressed")
	else:
		print("No buttons were pressed")

	
