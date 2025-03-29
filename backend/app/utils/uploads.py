import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder, width=None):
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{filename}"
    
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(upload_path, exist_ok=True)
    
    filepath = os.path.join(upload_path, filename)
    
    # Open and process the image
    image = Image.open(file)
    
    # Convert to RGB if necessary
    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
    
    # Resize if width is specified
    if width:
        ratio = width / image.size[0]
        height = int(image.size[1] * ratio)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
    
    # Save with optimized settings
    image.save(filepath, 'JPEG', quality=85, optimize=True)
    
    # Return the relative path for database storage
    return os.path.join(folder, filename)

def delete_image(filepath):
    if not filepath:
        return False
    
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
        return True
    except Exception as e:
        current_app.logger.error(f"Error deleting file {filepath}: {str(e)}")
        return False

def get_image_dimensions(filepath):
    if not filepath:
        return None, None
    
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
    try:
        with Image.open(full_path) as img:
            return img.size
    except Exception as e:
        current_app.logger.error(f"Error getting image dimensions for {filepath}: {str(e)}")
        return None, None 