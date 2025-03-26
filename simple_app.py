from flask import Flask, jsonify
import os

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    print(f"Flask app running on port {port}") 