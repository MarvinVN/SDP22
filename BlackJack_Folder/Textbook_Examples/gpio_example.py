from gpiozero import Button
import sys



# defining pin numbers
p1_hit_button = Button(2)
p1_stand_button = Button(3)
p1_double_button = Button(4)
p1_exit_button = Button(17)	

#testing button functionality
while(1):
	if p1_hit_button.is_pressed:
		#want to update the gui that event was detected; SLOT to eventDetected()
		print("P1 Hit Button was pressed")
	elif p1_stand_button.is_pressed:
		print("P1 Stand Button was pressed")
	elif p1_double_button.is_pressed:
		print("P1 Double Button was pressed")
	elif p1_exit_button.is_pressed:
		print("P1 Exit Button was pressed")
	else:
		print("No buttons were pressed")

	
