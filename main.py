import os
import sys
import queue

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

	audio_streamer = Audio_Streamer(
		out_queue = audio_to_signal_queue
	)
	signal_processor = Signal_Processor(
		in_queue = audio_to_signal_queue,
		out_queue = signal_to_gui_queue
	)
	gui = GUI(
		in_queue = signal_to_gui_queue
	)

	audio_streamer.start()
	signal_processor.start()
	gui.start()


if __name__ == "__main__":
	main()


