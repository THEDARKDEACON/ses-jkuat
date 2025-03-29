import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file, folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save and optimize image
        image = Image.open(file)
        image.save(filepath, optimize=True, quality=85)
        
        return os.path.join('uploads', folder, filename)
    return None

def delete_image(filepath):
    if filepath:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
        if os.path.exists(full_path):
            os.remove(full_path)

def format_date(date):
    return date.strftime('%B %d, %Y')

def truncate_text(text, length=150):
    if len(text) <= length:
        return text
    return text[:length] + '...' 