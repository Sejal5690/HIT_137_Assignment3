
import tkinter as tk

# Custom decorator example
def log_method_call(func):
	def wrapper(*args, **kwargs):
		print(f"Calling method: {func.__name__}")
		return func(*args, **kwargs)
	return wrapper

# Base class for window configuration
class WindowConfig:
	def __init__(self, title="OOP Tkinter GUI", size="400x300"):
		self._title = title  # Encapsulation: protected attribute
		self._size = size

	def get_title(self):
		return self._title

	def set_title(self, title):
		self._title = title

	def get_size(self):
		return self._size

	def set_size(self, size):
		self._size = size

# Base class for widget creation
class WidgetFactory:
	@staticmethod
	def create_label(master, text):
		return tk.Label(master, text=text)

	@staticmethod
	def create_entry(master):
		return tk.Entry(master)

	@staticmethod
	def create_button(master, text, command):
		return tk.Button(master, text=text, command=command)

# Main GUI class using multiple inheritance
class MainGUI(WindowConfig, WidgetFactory):
	def __init__(self):
		super().__init__()
		self._root = tk.Tk()
		self._root.title(self.get_title())
		self._root.geometry(self.get_size())
		self._user_input = None  # Encapsulation: private attribute
		self.setup_widgets()

	@log_method_call
	def setup_widgets(self):
		# Polymorphism: create_label from WidgetFactory
		label = self.create_label(self._root, "Enter your name:")
		label.pack(pady=10)
		self._user_input = self.create_entry(self._root)
		self._user_input.pack(pady=10)
		button = self.create_button(self._root, "Greet", self.greet_user)
		button.pack(pady=10)
		self._output_label = self.create_label(self._root, "")
		self._output_label.pack(pady=10)

	@log_method_call
	def greet_user(self):
		name = self._user_input.get()
		greeting = self.get_greeting(name)
		self._output_label.config(text=greeting)

	def get_greeting(self, name):
		# Method overriding demonstration: can be overridden in subclass
		return f"Hello, {name}! Welcome to OOP Tkinter GUI."

	def run(self):
		self._root.mainloop()

# Subclass to demonstrate method overriding and polymorphism
class CustomGUI(MainGUI):
	def get_greeting(self, name):
		# Overridden method
		return f"Hi, {name}! This is a custom greeting."

if __name__ == "__main__":
	# Polymorphism: can use either MainGUI or CustomGUI
	gui = MainGUI()
	# gui = CustomGUI()  # Uncomment to use overridden greeting
	gui.run()
