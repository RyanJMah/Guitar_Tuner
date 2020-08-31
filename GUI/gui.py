import os
import json
import queue
import time
import tkinter as tk
import tkinter.ttk as ttk

DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def closest(lst, K):
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 

class GUI():
	# I don't have to make this class a thread since tkinter
	# forces you to run mainloop in the main thread

	def __init__(self, root, in_queue):
		self.in_buffer = in_queue

		self.FREQ_TOLERANCE = 0.8
		with open(os.path.join(DIRECTORY, "note_map.json"), "r") as f:
			self.note_map = json.load(f)
			self.freqs_list = [float(i) for i in self.note_map.keys()]


		self.root = root
		self.root.geometry("500x310")
		self.root.title("Guitar Tuner")
		self.root.resizable(False, False)
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


		self.canvas = tk.Canvas(self.root)
		self.canvas.pack()

		self.note = self.canvas.create_text(180, 190, font = ("Roboto", 50), text = "-")
		self.too_flat = self.canvas.create_rectangle(0, 60, 0+50, 60+40, outline = "grey", fill = "grey")
		self.ok = self.canvas.create_text(180, 80, font = ("Roboto", 18, "bold"), fill = "grey", text = "OK")
		self.too_sharp = self.canvas.create_rectangle(315, 60, 310+53, 60+40, outline = "grey", fill = "grey")

		self._running = True
		self.update_gui()


	def on_closing(self):
		self._running = False
		time.sleep(0.5)
		self.root.destroy()

	def display_too_flat(self, is_flat):
		if is_flat:
			self.canvas.itemconfig(self.too_flat, fill = "red")		
		else:
			self.canvas.itemconfig(self.too_flat, fill = "grey")

	def display_too_sharp(self, is_sharp):
		if is_sharp:
			self.canvas.itemconfig(self.too_sharp, fill = "red")
		else:
			self.canvas.itemconfig(self.too_sharp, fill = "grey")

	def display_ok(self, is_ok):
		if is_ok:
			self.canvas.itemconfig(self.ok, fill = "green")
		else:
			self.canvas.itemconfig(self.ok, fill = "grey")

	def display_note(self, note):
		"""note is a string"""
		self.canvas.itemconfig(self.note, text = note)


	def update_gui(self):
		while self._running:
			self.root.update()
			if self.in_buffer.empty():
				continue

			freq = self.in_buffer.get()

			if freq < 80:
				# if the frequency is below 70Hz, it's just noise (the lowest
				# frequency on a guitar in standard tuning is 83.41 Hz)
				self.display_note("-")
				self.display_too_flat(False)
				self.display_too_sharp(False)
				self.display_ok(False)
				continue
			
			closest_freq = closest(self.freqs_list, freq)
			note = self.note_map["%.2f" % closest_freq]
			self.display_note(note)

			f_error = freq - closest_freq
			if (f_error < 0) and (abs(f_error) > self.FREQ_TOLERANCE):	# freq too low
				self.display_too_flat(True)
				self.display_too_sharp(False)
				self.display_ok(False)
			elif (f_error > 0) and (abs(f_error) > self.FREQ_TOLERANCE):	# freq too high
				self.display_too_flat(False)
				self.display_too_sharp(True)
				self.display_ok(False)
			else:
				self.display_too_flat(False)
				self.display_too_sharp(False)
				self.display_ok(True)




if __name__ == "__main__":
	signal_to_gui_queue = queue.Queue()

	root = tk.Tk()
	gui = GUI(root, signal_to_gui_queue)
	gui.root.mainloop()
