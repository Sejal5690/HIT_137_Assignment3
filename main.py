# Main file for Assignment 3 - With AI Models

import sys
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
        import torch
        import transformers
        import diffusers
        return True
    except ImportError as e:
        print(f"Missing basic dependency: {e}")
        print("Please install required packages:")
        print("pip install transformers diffusers torch Pillow")
        return False

def test_models():
    """Test the AI models are working."""
    try:
        from models.base_model import BaseAIModel
        from models.image_caption import ImageCaptionModel
        from models.text_to_image import TextToImageModel
        
        print("✓ All AI models imported successfully")
        
        # Test model creation (without loading)
        img_model = ImageCaptionModel()
        txt_model = TextToImageModel()
        
        print(f"✓ Image Caption Model: {img_model.model_name}")
        print(f"✓ Text-to-Image Model: {txt_model.model_name}")
        
        return True
    except Exception as e:
        print(f"Model test failed: {e}")
        return False

def main():
    # AI model testing
    print("=" * 60)
    print("AI Model Demo Application - HIT137 Assignment 3")
    print("AI Models Implementation Complete")
    print("=" * 60)
    
    if not check_basic_dependencies():
        print("Please install dependencies first.")
        sys.exit(1)
    
    if not test_models():
        print("AI model setup failed.")
        sys.exit(1)
    
    print("AI models ready for integration!")
    print("Next: GUI development...")

if __name__ == "__main__":
    main()