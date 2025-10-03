"""
File handling utilities with encapsulation demonstration.

This module showcases:
- Encapsulation through private methods and properties
- Error handling and data validation
- Clean separation of file I/O concerns
"""

import os
from pathlib import Path
from typing import Optional, List
from PIL import Image
import tkinter.filedialog as fd


class FileHandler:
    """
    File operations handler with encapsulated functionality.
    
    Demonstrates encapsulation by hiding file operation complexity
    behind a clean interface. Private methods handle internal logic
    while public methods provide safe access to functionality.
    """
    
    def __init__(self):
        """Initialize file handler with private state tracking."""
        self._last_directory = Path.home()  # Private attribute - encapsulation
        self._supported_image_formats = {  # Private configuration - encapsulation
            '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'
        }
        self._supported_text_formats = {
            '.txt', '.md', '.rst'
        }
    
    @property
    def last_directory(self) -> Path:
        """Get last used directory - encapsulated property access."""
        return self._last_directory
    
    @property
    def supported_image_formats(self) -> set:
        """Get supported image formats - encapsulated configuration."""
        return self._supported_image_formats.copy()  # Return copy to prevent modification
    
    def _is_valid_image_file(self, file_path: Path) -> bool:
        """
        Private method to validate image file - encapsulation.
        
        Args:
            file_path: Path to image file
            
        Returns:
            True if file is a valid image format
        """
        return file_path.suffix.lower() in self._supported_image_formats
    
    def _update_last_directory(self, file_path: Path) -> None:
        """
        Private method to update last used directory - encapsulation.
        
        Args:
            file_path: Path to update from
        """
        if file_path.parent.exists():
            self._last_directory = file_path.parent
    
    def browse_image_file(self) -> Optional[Path]:
        """
        Open file dialog to select image file.
        
        Encapsulates file dialog complexity and validation.
        
        Returns:
            Path to selected image file or None if cancelled
        """
        filetypes = [
            ('Image files', '*.jpg *.jpeg *.png *.bmp *.tiff *.webp'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('PNG files', '*.png'),
            ('All files', '*.*')
        ]
        
        file_path = fd.askopenfilename(
            title="Select Image File",
            initialdir=str(self._last_directory),
            filetypes=filetypes
        )
        
        if file_path:
            path_obj = Path(file_path)
            if self._is_valid_image_file(path_obj):
                self._update_last_directory(path_obj)
                return path_obj
            else:
                raise ValueError(f"Unsupported image format: {path_obj.suffix}")
        
        return None
    
    def load_image(self, file_path: Path) -> Image.Image:
        """
        Load image file with validation - encapsulated error handling.
        
        Args:
            file_path: Path to image file
            
        Returns:
            PIL Image object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format not supported
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        if not self._is_valid_image_file(file_path):
            raise ValueError(f"Unsupported image format: {file_path.suffix}")
        
        try:
            image = Image.open(file_path)
            # Convert to RGB if needed (handles RGBA, etc.)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")
    
    def save_image(self, image: Image.Image, suggested_name: str = "generated_image") -> Optional[Path]:
        """
        Save image with file dialog - encapsulated save operation.
        
        Args:
            image: PIL Image to save
            suggested_name: Default filename suggestion
            
        Returns:
            Path where image was saved or None if cancelled
        """
        filetypes = [
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg'),
            ('All files', '*.*')
        ]
        
        file_path = fd.asksaveasfilename(
            title="Save Image As",
            initialdir=str(self._last_directory),
            initialfile=suggested_name,
            defaultextension=".png",
            filetypes=filetypes
        )
        
        if file_path:
            try:
                path_obj = Path(file_path)
                image.save(path_obj, quality=95)
                self._update_last_directory(path_obj)
                return path_obj
            except Exception as e:
                raise ValueError(f"Failed to save image: {str(e)}")
        
        return None
    
    def save_text(self, text: str, suggested_name: str = "caption") -> Optional[Path]:
        """
        Save text content with file dialog - encapsulated text save.
        
        Args:
            text: Text content to save
            suggested_name: Default filename suggestion
            
        Returns:
            Path where text was saved or None if cancelled
        """
        filetypes = [
            ('Text files', '*.txt'),
            ('Markdown files', '*.md'),
            ('All files', '*.*')
        ]
        
        file_path = fd.asksaveasfilename(
            title="Save Text As",
            initialdir=str(self._last_directory),
            initialfile=suggested_name,
            defaultextension=".txt",
            filetypes=filetypes
        )
        
        if file_path:
            try:
                path_obj = Path(file_path)
                with open(path_obj, 'w', encoding='utf-8') as f:
                    f.write(text)
                self._update_last_directory(path_obj)
                return path_obj
            except Exception as e:
                raise ValueError(f"Failed to save text: {str(e)}")
        
        return None
    
    def get_file_info(self, file_path: Path) -> dict:
        """
        Get information about a file - encapsulated file analysis.
        
        Args:
            file_path: Path to analyze
            
        Returns:
            Dictionary with file information
        """
        if not file_path.exists():
            return {"exists": False}
        
        stat = file_path.stat()
        return {
            "exists": True,
            "name": file_path.name,
            "size_bytes": stat.st_size,
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "extension": file_path.suffix.lower(),
            "is_image": self._is_valid_image_file(file_path),
            "modified": stat.st_mtime
        }