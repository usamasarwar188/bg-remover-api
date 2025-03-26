#!/usr/bin/env python3
"""
Script to pre-download models for rembg.
This script is called during the build phase to ensure models are available
when the app starts.
"""
print("Starting model download...")

try:
    # This import will trigger model downloads
    from rembg import remove
    import numpy as np
    from PIL import Image
    
    # Create a small image and run remove on it to ensure models are downloaded
    img = Image.new('RGB', (100, 100), color='white')
    output = remove(img)
    
    print("✅ Models successfully downloaded and verified!")
except Exception as e:
    print(f"❌ Error downloading models: {str(e)}")
    # Don't raise the exception - we want the build to continue
    
print("Model download script completed.") 