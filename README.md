# BG Remover - Backend API

Flask backend API for the BG Remover application that provides image background removal functionality.

## Features

- Remove backgrounds from images using the rembg library
- Apply solid color backgrounds
- Apply image backgrounds
- RESTful API design

## Tech Stack

- Flask: Web framework
- rembg: Background removal library
- Pillow: Image processing
- Gunicorn: WSGI HTTP Server
- Flask-CORS: Cross-Origin Resource Sharing

## Local Development

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file based on `.env.sample`:
   ```bash
   cp .env.sample .env
   ```
6. Run the development server:
   ```bash
   python app.py
   ```

The server will be available at http://localhost:5001.

## API Endpoints

### Health Check

```
GET /
GET /health
```

Returns server status information.

### Remove Background

```
POST /remove-background
POST /remove-bg
```

Removes the background from an uploaded image.

**Parameters:**

- `file`: The image file to process (required)

**Returns:**

- PNG image with transparent background

### Process Image

```
POST /process-image
```

Removes the background and optionally applies a new background.

**Parameters:**

- `file`: The image file to process (required)
- `bg_type`: Type of background to apply (`transparent`, `color`, or `image`)
- `bg_color`: Hex color code when `bg_type` is `color`
- `bg_image`: Background image file when `bg_type` is `image`

**Returns:**

- PNG image with the processed result

## Deployment

### Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Select the branch to deploy
4. Use the following settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app -c gunicorn_config.py`
5. Add environment variables:
   - `FLASK_ENV`: `production`
   - `ALLOWED_ORIGINS`: Comma-separated list of frontend domain(s)

### Heroku

1. Install the Heroku CLI and login
2. Initialize a git repository if not already done
3. Add Heroku as a remote:
   ```bash
   heroku create bg-remover-api
   ```
4. Set environment variables:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```
5. Deploy:
   ```bash
   git push heroku main
   ```

## License

MIT
