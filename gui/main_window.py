# Main GUI window for Assignment 3

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
from pathlib import Path
from typing import Optional, Dict, Any
import threading
import time

from gui.widgets import ImageDisplayFrame, StatusBar, ScrollableInfoFrame
from gui.decorators import validate_input, log_operation, error_handler
from models.text_to_image import TextToImageModel
from models.image_caption import ImageCaptionModel
from utils.file_handler import FileHandler
from utils.logger import logger


class ModelManager:
    # Handles the AI models
    
    def __init__(self):
        # Set up the models
        self._text_to_image_model: Optional[TextToImageModel] = None
        self._image_caption_model: Optional[ImageCaptionModel] = None
        self._model_cache: Dict[str, Any] = {}
        self._current_mode = "text_to_image"
    
    @property
    def current_mode(self) -> str:
        # Return current mode
        return self._current_mode
    
    def _get_text_to_image_model(self) -> TextToImageModel:
        # Load text to image model
        if self._text_to_image_model is None:
            logger.info("Initializing Text-to-Image model")
            self._text_to_image_model = TextToImageModel()
        return self._text_to_image_model
    
    def _get_image_caption_model(self) -> ImageCaptionModel:
        # Load image caption model
        if self._image_caption_model is None:
            logger.info("Initializing Image Caption model")
            self._image_caption_model = ImageCaptionModel()
        return self._image_caption_model
    
    @log_operation
    def process_text_to_image(self, text_prompt: str) -> Image.Image:
        # Make image from text
        model = self._get_text_to_image_model()
        return model.process(text_prompt)
    
    @log_operation
    def process_image_to_caption(self, image: Image.Image) -> str:
        # Make caption from image
        model = self._get_image_caption_model()
        return model.process(image)


class MainWindow(tk.Tk, ModelManager):
    # Main window class with multiple inheritance
    
    def __init__(self):
        # Set up the main window
        tk.Tk.__init__(self)
        ModelManager.__init__(self)
        
        self._file_handler = FileHandler()
        self._selected_image_path: Optional[str] = None
        
        self.title("Assignment 3")
        self.state('zoomed')
        self.configure(bg='#f0f0f0')
        
        self._create_widgets()
        self._setup_layout()
        self._setup_event_handlers()
        self._on_mode_change()
        
        logger.log_user_action("Application started")
    
    def _create_widgets(self) -> None:
        # Create GUI widgets
        
        # Title label
        self.title_label = tk.Label(
            self,
            text="Assignment 3 - AI Models",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        
        # Mode selection frame
        self.mode_frame = tk.Frame(self, bg='#f0f0f0')
        self.mode_label = tk.Label(
            self.mode_frame,
            text="Select Mode:",
            font=('Arial', 12),
            bg='#f0f0f0'
        )
        self.mode_combo = ttk.Combobox(
            self.mode_frame,
            values=["Text to Image", "Image to Caption"],
            state="readonly",
            width=20
        )
        self.mode_combo.set("Text to Image")
        
        # Main content frame
        self.content_frame = tk.Frame(self, bg='#f0f0f0')
        
        # Input section
        self.input_frame = tk.LabelFrame(
            self.content_frame,
            text="Input",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        
        # Text input
        self.text_input = tk.Text(
            self.input_frame,
            height=4,
            width=40,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        
        # Image input
        self.image_input_frame = tk.Frame(self.input_frame, bg='#f0f0f0')
        self.browse_button = tk.Button(
            self.image_input_frame,
            text="Browse Image...",
            font=('Arial', 10),
            command=self._browse_image
        )
        self.image_path_label = tk.Label(
            self.image_input_frame,
            text="No image selected",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#666666'
        )
        
        # Process button
        self.process_button = tk.Button(
            self.input_frame,
            text="Generate",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            command=self._process_input
        )
        
        # Output section
        self.output_frame = tk.LabelFrame(
            self.content_frame,
            text="Output",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        
        # Image display
        self.image_display = ImageDisplayFrame(self.output_frame, max_width=512, max_height=512)
        
        # Text output
        self.text_output = tk.Text(
            self.output_frame,
            height=6,
            width=40,
            wrap=tk.WORD,
            font=('Arial', 10),
            state=tk.DISABLED
        )
        
        # Save button
        self.save_button = tk.Button(
            self.output_frame,
            text="Save Result",
            font=('Arial', 10),
            command=self._save_result,
            state=tk.DISABLED
        )
        
        # Info sections container
        self.info_container = tk.Frame(self, bg='#f0f0f0')
        
        # Current model information (updates based on selection)
        self.current_model_info = ScrollableInfoFrame(
            self.info_container,
            title="Current Model Information"
        )
        
        # OOP Concepts explanation
        self.oop_concepts_info = ScrollableInfoFrame(
            self.info_container,
            title="OOP Concepts Demonstration"
        )
        
        # Status bar
        self.status_bar = StatusBar(self)
        
        # Set initial information content
        self._setup_oop_concepts_info()
        self._update_current_model_info()
    
    def _setup_layout(self) -> None:
        # Arrange widgets
        
        # Title
        self.title_label.pack(pady=10)
        
        # Mode selection
        self.mode_frame.pack(fill=tk.X, padx=20, pady=5)
        self.mode_label.pack(side=tk.LEFT, padx=(0, 10))
        self.mode_combo.pack(side=tk.LEFT)
        
        # Main content area
        self.content_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Input and output frames side by side
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Input widgets
        self.text_input.pack(pady=5)
        
        self.image_input_frame.pack(pady=5)
        self.browse_button.pack()
        self.image_path_label.pack(pady=(5, 0))
        
        self.process_button.pack(pady=10)
        
        # Output widgets
        self.image_display.pack(pady=5)
        self.text_output.pack(pady=5)
        self.save_button.pack(pady=10)
        
        # Information sections container
        self.info_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 10))
        
        # Pack info sections side by side
        self.current_model_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.oop_concepts_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Status bar
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _setup_event_handlers(self) -> None:
        # Setup event handlers
        self.mode_combo.bind('<<ComboboxSelected>>', lambda e: self._on_mode_change())
    
    def _on_mode_change(self) -> None:
        # Handle mode change
        selected = self.mode_combo.get()
        
        if selected == "Text to Image":
            self._current_mode = "text_to_image"
            self.text_input.pack(pady=5)
            self.image_input_frame.pack_forget()
            self.process_button.config(text="Generate Image")
            
        elif selected == "Image to Caption":
            self._current_mode = "image_to_caption"
            self.text_input.pack_forget()
            self.image_input_frame.pack(pady=5)
            self.process_button.config(text="Generate Caption")
        
        # Update model information based on selection
        self._update_current_model_info()
        
        # Clear previous results
        self._clear_output()
        
        logger.log_user_action(f"Mode changed to: {selected}")
    
    @error_handler("Failed to browse image")
    def _browse_image(self) -> None:
        # Browse for image file
        try:
            image_path = self._file_handler.browse_image_file()
            if image_path:
                self._selected_image_path = str(image_path)
                filename = image_path.name
                self.image_path_label.config(text=filename, fg='#333333')
                
                # Show preview
                image = self._file_handler.load_image(image_path)
                self.image_display.display_image(image)
                
                logger.log_user_action(f"Image selected: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    @validate_input
    @log_operation
    @error_handler("Processing failed")
    def _process_input(self) -> None:
        # Process user input using threading to prevent GUI freeze
        
        # Validate input first
        try:
            if self._current_mode == "text_to_image":
                text_prompt = self.text_input.get(1.0, tk.END).strip()
                if not text_prompt:
                    raise ValueError("Please enter a text prompt")
            elif self._current_mode == "image_to_caption":
                if not self._selected_image_path:
                    raise ValueError("Please select an image file")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        
        # Start processing in background thread
        self._start_processing_thread()
    
    def _start_processing_thread(self) -> None:
        # Start background processing thread
        self.process_button.config(state=tk.DISABLED, text="Processing...")
        self.save_button.config(state=tk.DISABLED)
        self.status_bar.set_status("Processing...")
        
        # Create and start processing thread
        processing_thread = threading.Thread(target=self._process_in_background, daemon=True)
        processing_thread.start()
    
    def _process_in_background(self) -> None:
        # Background processing method
        try:
            if self._current_mode == "text_to_image":
                # Get text input
                text_prompt = self.text_input.get(1.0, tk.END).strip()
                
                # Generate image
                image = self.process_text_to_image(text_prompt)
                
                # Schedule GUI update in main thread
                self.after(0, lambda: self._display_image_result(image, text_prompt))
                
            elif self._current_mode == "image_to_caption":
                # Load image
                image_path = Path(self._selected_image_path)
                
                image = self._file_handler.load_image(image_path)
                
                # Generate caption
                caption = self.process_image_to_caption(image)
                
                # Schedule GUI update in main thread
                self.after(0, lambda: self._display_text_result(caption))
            
            # Schedule final cleanup in main thread
            self.after(0, self._processing_complete)
            
        except Exception as e:
            # Schedule error handling in main thread
            self.after(0, lambda: self._processing_error(str(e)))
    
    def _display_image_result(self, image: Image.Image, prompt: str) -> None:
        # Display image result in main thread
        self.image_display.display_image(image)
        self._set_text_output(f"Generated image from prompt: '{prompt}'")
    
    def _display_text_result(self, caption: str) -> None:
        # Display text result in main thread
        self._set_text_output(caption)
    
    def _processing_complete(self) -> None:
        # Complete processing and reset UI
        self.status_bar.set_status("Ready")
        self.process_button.config(state=tk.NORMAL, text="Generate")
        self.save_button.config(state=tk.NORMAL)
    
    def _processing_error(self, error_msg: str) -> None:
        # Handle processing error
        messagebox.showerror("Error", error_msg)
        self.status_bar.set_status("Ready")
        self.process_button.config(state=tk.NORMAL, text="Generate")
    
    @error_handler("Failed to save result")
    def _save_result(self) -> None:
        # Save the result
        try:
            if self._current_mode == "text_to_image":
                # Save image
                current_image = self.image_display.get_current_image()
                if current_image:
                    saved_path = self._file_handler.save_image(current_image, "generated_image")
                    if saved_path:
                        messagebox.showinfo("Success", f"Image saved to: {saved_path.name}")
                        logger.log_user_action(f"Image saved: {saved_path}")
            
            elif self._current_mode == "image_to_caption":
                # Save caption text
                caption = self.text_output.get(1.0, tk.END).strip()
                if caption:
                    saved_path = self._file_handler.save_text(caption, "image_caption")
                    if saved_path:
                        messagebox.showinfo("Success", f"Caption saved to: {saved_path.name}")
                        logger.log_user_action(f"Caption saved: {saved_path}")
                        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _clear_output(self) -> None:
        # Clear output display
        self.image_display.clear_image()
        self._set_text_output("")
        self.save_button.config(state=tk.DISABLED)
    
    def _set_text_output(self, text: str) -> None:
        # Set text output
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, text)
        self.text_output.config(state=tk.DISABLED)
    

    
    def _update_current_model_info(self) -> None:
        # Update model info based on current selection
        if self._current_mode == "text_to_image":
            model_text = """Model Name: Stable Diffusion v1.5
Category: Text to Image
Description: Creates images from text descriptions. Takes about 15-30 seconds to generate a 512x512 image."""
        
        else:  # image_to_caption
            model_text = """Model Name: BLIP Image Captioning
Category: Vision
Description: Analyzes images and writes text descriptions. Takes about 3-8 seconds to process most images."""
        
        self.current_model_info.set_content(model_text)
    
    def _setup_oop_concepts_info(self) -> None:
        # Set up OOP concepts explanation
        oop_text = """OOP Concepts Used:

1. Multiple Inheritance:
MainWindow class inherits from tk.Tk and ModelManager classes. This means it gets features from both parent classes.

2. Encapsulation:
Methods with underscore like _process_input are private. This hides internal details from other parts of the program.

3. Polymorphism and Method Overriding:
Both AI models have a process() method but they do different things. TextToImageModel makes images, ImageCaptionModel makes text.

4. Multiple Decorators:
We use @validate_input to check inputs, @log_operation to record actions, @error_handler to catch errors, and @cache_result to save results."""
        
        self.oop_concepts_info.set_content(oop_text)