from flask import Flask, jsonify , request, send_file
import os
import io
from PIL import Image
import numpy as np

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

app = Flask(__name__)

@app.route('/')
def index():
    port = os.environ.get('PORT', '5000')
    return jsonify({
        "status": "success",
        "message": "Simple Flask app is running!",
        "port": port,
        "environment": os.environ.get('FLASK_ENV', 'development')
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# @app.route("/remove-bg", methods=["POST"])
# @app.route("/remove-background", methods=["POST"])
# def remove_background():
#     """Remove background from an image."""
#     # Check if file is present
#     if "file" not in request.files:
#         return jsonify({"error": "No file part"}), 400
        
#     input_image_file = request.files.get("file")
    
#     # Check if filename is empty
#     if input_image_file.filename == "":
#         return jsonify({"error": "No selected file"}), 400
    
#     try:
#         if not REMBG_AVAILABLE:
#             # If rembg is not available, just return a dummy transparent PNG
#             img = Image.new('RGBA', (300, 300), (0, 0, 0, 0))
#             img_io = io.BytesIO()
#             img.save(img_io, format='PNG')
#             img_io.seek(0)
#             return send_file(img_io, mimetype='image/png')
        
#         # Process the image - remove background
#         input_image = Image.open(input_image_file).convert("RGBA")
#         removed_bg_image = remove(input_image)
        
#         # Save the processed image in-memory
#         img_io = io.BytesIO()
#         removed_bg_image.save(img_io, format="PNG")
#         img_io.seek(0)
        
#         return send_file(img_io, mimetype="image/png")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    print(f"Flask app running on port {port}") 