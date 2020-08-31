import os
import sys
import queue
import tkinter as tk

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(DIRECTORY, "Audio-Streaming"))
sys.path.append(os.path.join(DIRECTORY, "Signal-Processing"))
sys.path.append(os.path.join(DIRECTORY, "GUI"))

from audio_streamer import Audio_Streamer
from signal_processor import Signal_Processor
from gui import GUI


def main():
	audio_to_signal_queue = queue.Queue()
	signal_to_gui_queue = queue.Queue()

	audio_streamer = Audio_Streamer(out_queue = audio_to_signal_queue)
	signal_processor = Signal_Processor(
		in_queue = audio_to_signal_queue,
		out_queue = signal_to_gui_queue
	)

	audio_streamer.start()
	signal_processor.start()

	try:
		root = tk.Tk()
		gui = GUI(root = root, in_queue = signal_to_gui_queue)
		gui.root.mainloop()
	except tk.TclError:
		pass

	# since audio_streamer and signal_processor are daemon threads, if we just exit here,
	# the above two threads will automatically exit as well.
	exit()


if __name__ == "__main__":
	main()


