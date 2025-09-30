import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import Menu

"""
Message from Mohamed: I have made ONLY the layout for the buttons and so, we'll have
to add functionality from now on, keep in mind i used chatgpt for some code references and
spelling checks.

--- Push 2

"""

# Custom decorator example
def log_method_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling method: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


class WindowConfig:
    def __init__(self, title="Tkinter AI GUI", size="800x600"):
        self._title = title
        self._size = size

    def get_title(self):
        return self._title

    def get_size(self):
        return self._size


class WidgetFactory:
    @staticmethod
    def create_label(master, text, font=None):
        return tk.Label(master, text=text, font=font)

    @staticmethod
    def create_entry(master):
        return tk.Entry(master)

    @staticmethod
    def create_button(master, text, command):
        return tk.Button(master, text=text, command=command)


class MainGUI(WindowConfig, WidgetFactory):
    def __init__(self):
        super().__init__()
        self._root = tk.Tk()
        self._root.title(self.get_title())
        self._root.geometry(self.get_size())

        self._user_input = None
        self._input_path = None
        self._input_type = tk.StringVar(value="Text")

        self.setup_widgets()

    @log_method_call
    def setup_widgets(self):
        # ---------------- Menu Bar ---------------- #
        menu_bar = Menu(self._root)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self._root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        models_menu = Menu(menu_bar, tearoff=0)
        models_menu.add_command(label="Model 1")
        models_menu.add_command(label="Model 2")
        menu_bar.add_cascade(label="Models", menu=models_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About")
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self._root.config(menu=menu_bar)

        # ---------------- Main Frame ---------------- #
        main_frame = tk.Frame(self._root, padx=8, pady=8)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---- Model Selection ---- #
        model_frame = tk.LabelFrame(main_frame, text="Model Selection", padx=8, pady=8)
        model_frame.pack(fill=tk.X, pady=5)

        self.model_selection_dropdown = ttk.Combobox(
            model_frame, values=["Text-to-Image", "Image Classification"], width=30
        )
        self.model_selection_dropdown.grid(row=0, column=0, padx=5)

        self.load_model_button = tk.Button(model_frame, text="Load Model", command=self.load_model, width=12)
        self.load_model_button.grid(row=0, column=1, padx=5)

        # ---- Middle Row: User Input + Output ---- #
        middle_frame = tk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # User Input Section
        input_frame = tk.LabelFrame(middle_frame, text="User Input Section", padx=8, pady=8)
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Radiobutton(input_frame, text="Text", variable=self._input_type, value="Text",
                       command=self.update_input).grid(row=0, column=0, sticky=tk.W, padx=5)
        tk.Radiobutton(input_frame, text="Image", variable=self._input_type, value="Image",
                       command=self.update_input).grid(row=0, column=1, sticky=tk.W, padx=5)

        self._user_input = tk.Entry(input_frame, width=40)
        self._user_input.grid(row=1, column=0, columnspan=2, pady=5)

        self.browse_button = tk.Button(input_frame, text="Browse", command=self.choose_file, width=12)
        self.browse_button.grid(row=1, column=0, columnspan=2, pady=5)
        self.browse_button.grid_remove()

        run_frame = tk.Frame(input_frame)
        run_frame.grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(run_frame, text="Run Model 1", command=self.run_model, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(run_frame, text="Run Model 2", command=self.run_model, width=15).pack(side=tk.LEFT, padx=5)

        # Model Output Section
        output_frame = tk.LabelFrame(middle_frame, text="Model Output Section", padx=8, pady=8)
        output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.output_display = tk.Text(output_frame, height=12, wrap=tk.WORD)
        self.output_display.pack(fill=tk.BOTH, expand=True)

        # ---- Model Info & Explanation ---- #
        info_frame = tk.LabelFrame(main_frame, text="Model Information & Explanation", padx=8, pady=8)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        left_info = tk.LabelFrame(info_frame, text="Selected Model Info", padx=8, pady=8)
        left_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(left_info, text="- Model Name").pack(anchor=tk.W)
        tk.Label(left_info, text="- Category (Text, Vision, Audio)").pack(anchor=tk.W)
        tk.Label(left_info, text="- Short Description").pack(anchor=tk.W)

        right_info = tk.LabelFrame(info_frame, text="OOP Concepts Explanation", padx=8, pady=8)
        right_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(right_info, text="• Where Multiple Inheritance applied").pack(anchor=tk.W)
        tk.Label(right_info, text="• Why Encapsulation was applied").pack(anchor=tk.W)
        tk.Label(right_info, text="• How Polymorphism & Method Overriding are shown").pack(anchor=tk.W)
        tk.Label(right_info, text="• Where Multiple Decorators are applied").pack(anchor=tk.W)

        # ---- Notes Section ---- #
        notes_frame = tk.LabelFrame(main_frame, text="Notes", padx=8, pady=8)
        notes_frame.pack(fill=tk.X, pady=5)
        tk.Label(notes_frame, text="Notes section").pack(anchor=tk.W)

    def update_input(self):
        if self._input_type.get() == "Text":
            self._user_input.grid(row=1, column=0, columnspan=2, pady=5)
            self.browse_button.grid_remove()
        else:
            self._user_input.grid_remove()
            self.browse_button.grid(row=1, column=0, columnspan=2, pady=5)

    def choose_file(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self._input_path = path
            self.output_display.insert(tk.END, f"Selected file: {path}\n")

    def load_model(self):
        self.output_display.insert(tk.END, "Model loaded.\n")

    def run_model(self):
        self.output_display.insert(tk.END, "Running Model...\n")

    def run(self):
        self._root.mainloop()


if __name__ == "__main__":
    gui = MainGUI()
    gui.run()
