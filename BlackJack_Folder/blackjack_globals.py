import multiprocessing as mp

gui_to_bj_queue = mp.Queue()	# gui write, blackjack read
bj_to_gui_queue = mp.Queue()	# blackjack write, gui read

game_process = None
terminated = False

# exclusively for GUI use
def writeBjQueue(data):
	gui_to_bj_queue.put(data)

# exclusively for BJ use
def readBjQueue():
	msg = gui_to_bj_queue.get()
	return msg

# exclusive for BJ use
def writeGuiQueue(data):
	bj_to_gui_queue.put(data)

# exclusively for GUI use
def readGuiQueue():
	msg = bj_to_gui_queue.get()
	return msg