# Main file for Assignment 3

import sys
import traceback
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def check_basic_dependencies():
    """Check if basic dependencies are available."""
    try:
        import tkinter
        from PIL import Image
        return True
    except ImportError as e:
        print(f"Missing basic dependency: {e}")
        print("Please install required packages:")
        print("pip install Pillow")
        return False

def import_application_modules():
    """Import application modules with better error handling."""
    try:
        print("Loading GUI modules...")
        from gui.main_window import MainWindow
        from utils.logger import logger
        print("✓ All modules loaded successfully")
        return MainWindow, logger
    except ImportError as e:
        print(f"Import Error in application modules: {e}")
        print("\nThis might be due to:")
        print("1. Missing AI libraries - run: pip install transformers diffusers torch")
        print("2. Module syntax errors - check the error message above")
        print("3. Incorrect working directory - make sure you're in the project root")
        return None, None
    except Exception as e:
        print(f"Unexpected error loading modules: {e}")
        traceback.print_exc()
        return None, None

# Check basic dependencies first
if not check_basic_dependencies():
    sys.exit(1)

# Try to import application modules
MainWindow, logger = import_application_modules()
if MainWindow is None:
    print("\nTo test basic imports, run: python test_imports.py")
    sys.exit(1)


def main():
    # Start the app
    try:
        # Create and start the GUI
        logger.info("Starting AI Model Demo Application")
        
        app = MainWindow()
        
        logger.info("GUI initialized successfully")
        
        # Run the app
        app.mainloop()
        
        logger.info("Application closed successfully")
        
    except Exception as e:
        # Handle any startup errors gracefully
        error_msg = f"Failed to start application: {str(e)}"
        logger.error(error_msg)
        print(f"ERROR: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Show error message
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Application Error", 
                f"Failed to start the application.\n\nError: {str(e)}\n\n"
                "Please ensure all dependencies are installed:\n"
                "pip install transformers diffusers torch Pillow"
            )
        except:
            pass
        
        sys.exit(1)


def check_dependencies():
    # Check if required packages are installed
    required_packages = [
        ('torch', 'PyTorch'),
        ('transformers', 'Hugging Face Transformers'),
        ('diffusers', 'Hugging Face Diffusers'),
        ('PIL', 'Pillow (PIL)'),
        ('tkinter', 'Tkinter (usually built-in)')
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            logger.info(f"[OK] {description} available")
        except ImportError:
            missing_packages.append(description)
            logger.error(f"[MISSING] {description} not found")
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nTo install missing packages:")
        print("pip install transformers diffusers torch Pillow")
        return False
    
    return True


if __name__ == "__main__":
    # Run the app
    print("=" * 60)
    print("AI Model Demo Application - HIT137 Assignment 3")
    print("Demonstrating OOP Concepts with Hugging Face Models")
    print("=" * 60)
    
    # Check dependencies before starting
    print("\nChecking dependencies...")
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        sys.exit(1)
    
    print("\nAll dependencies available. Starting application...\n")
    
    # Start the main application
    main()