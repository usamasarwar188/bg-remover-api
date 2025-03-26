from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image, ImageDraw
import io
import os
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS based on environment
if os.environ.get('FLASK_ENV') == 'production':
    # In production, specify allowed origins
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
    CORS(app, resources={r"/*": {"origins": allowed_origins}})
else:
    # In development, allow all origins
    CORS(app)

# Define upload folder - use environment variable or default
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists

@app.route('/')
def index():
    """Health check endpoint."""
    return jsonify({
        "status": "Server is running",
        "version": "1.0.0",
        "message": "Use POST /process-image endpoint for image processing"
    })

@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "healthy"})

def hex_to_rgba(hex_color, opacity=255):
    """Convert hex color (without #) to RGBA tuple."""
    # Remove # if present
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (*rgb, opacity)

def create_gradient(size, start_color, end_color, direction='horizontal'):
    """Create a gradient image."""
    width, height = size
    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)
    
    # Unpack RGBA values
    start_r, start_g, start_b, start_a = start_color
    end_r, end_g, end_b, end_a = end_color
    
    for i in range(width if direction == 'horizontal' else height):
        # Calculate the ratio for color interpolation
        ratio = i / (width - 1) if direction == 'horizontal' else i / (height - 1)
        
        # Interpolate between start and end colors
        current_r = int(start_r * (1 - ratio) + end_r * ratio)
        current_g = int(start_g * (1 - ratio) + end_g * ratio)
        current_b = int(start_b * (1 - ratio) + end_b * ratio)
        current_a = int(start_a * (1 - ratio) + end_a * ratio)
        
        current_color = (current_r, current_g, current_b, current_a)
        
        if direction == 'horizontal':
            draw.line([(i, 0), (i, height)], fill=current_color)
        else:
            draw.line([(0, i), (width, i)], fill=current_color)
            
    return image

@app.route("/process-image", methods=["POST"])
def process_image():
    """Process an image to remove background and optionally apply a new background."""
    try:
        # Check if file is present
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
            
        input_image_file = request.files.get("file")
        
        # Check if filename is empty
        if input_image_file.filename == "":
            return jsonify({"error": "No selected file"}), 400
            
        # Get background type
        bg_type = request.form.get("bg_type", "transparent")
        
        # Process the image - remove background
        input_image = Image.open(input_image_file).convert("RGBA")
        removed_bg_image = remove(input_image)
        
        # Apply new background if needed
        if bg_type == "image" and "bg_image" in request.files:
            # Use uploaded background image
            bg_image_file = request.files.get("bg_image")
            background = Image.open(bg_image_file).convert("RGBA")
            
            # Resize background to match foreground if needed
            if background.size != removed_bg_image.size:
                background = background.resize(removed_bg_image.size, Image.Resampling.LANCZOS)
                
            # Create a composite
            composite = Image.alpha_composite(background, removed_bg_image)
            result_image = composite
            
        elif bg_type == "color" and "bg_color" in request.form:
            # Use color background
            bg_color = request.form.get("bg_color").lstrip('#')
            try:
                # Convert hex color to RGBA
                bg_color_rgba = hex_to_rgba(bg_color)
                
                # Create a solid color background
                background = Image.new("RGBA", removed_bg_image.size, bg_color_rgba)
                
                # Create a composite
                composite = Image.alpha_composite(background, removed_bg_image)
                result_image = composite
            except ValueError:
                # If color conversion fails, return transparent
                result_image = removed_bg_image
        else:
            # Return with transparent background
            result_image = removed_bg_image
        
        # Convert to PNG and save to memory
        img_io = io.BytesIO()
        result_image.save(img_io, format="PNG")
        img_io.seek(0)
        
        return send_file(img_io, mimetype="image/png")
        
    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/remove-background", methods=["POST"])
@app.route("/remove-bg", methods=["POST"])  # Alias for frontend compatibility
def remove_background():
    """Remove background from an image."""
    # Get uploaded file
    input_image_file = request.files.get("file")

    if not input_image_file:
        return jsonify({"error": "Input image is required"}), 400

    try:
        app.logger.info("Removing background from image")
        # Open input image and remove background
        input_image = Image.open(input_image_file).convert("RGBA")
        removed_bg_image = remove(input_image)

        # Save the processed image in-memory
        img_io = io.BytesIO()
        removed_bg_image.save(img_io, format="PNG")
        img_io.seek(0)

        app.logger.info("Background removal complete")
        return send_file(img_io, mimetype="image/png")
    except Exception as e:
        app.logger.error(f"Error removing background: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host="0.0.0.0", debug=debug, port=port) 