from wtforms.validators import ValidationError
import re

def validate_password(form, field):
    """
    Validate password strength:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
    password = field.data
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')
    
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter')
    
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one number')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character')

def validate_username(form, field):
    """
    Validate username:
    - Between 3 and 20 characters long
    - Contains only letters, numbers, and underscores
    - Starts with a letter
    """
    username = field.data
    if not 3 <= len(username) <= 20:
        raise ValidationError('Username must be between 3 and 20 characters long')
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        raise ValidationError('Username must start with a letter and contain only letters, numbers, and underscores')

def validate_phone(form, field):
    """
    Validate phone number format:
    - Must be a valid international phone number
    """
    phone = field.data
    if not re.match(r'^\+?1?\d{9,15}$', phone):
        raise ValidationError('Invalid phone number format')

def validate_image(form, field):
    """
    Validate image file:
    - Must be a valid image file type
    - Must not exceed maximum file size
    """
    if not field.data:
        return
    
    filename = field.data.filename.lower()
    if not any(filename.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
        raise ValidationError('Invalid image format. Allowed formats: JPG, JPEG, PNG, GIF')
    
    # Check file size (max 5MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
    field.data.seek(0, 2)  # Seek to end of file
    size = field.data.tell()  # Get current position (file size)
    field.data.seek(0)  # Seek back to start
    
    if size > MAX_FILE_SIZE:
        raise ValidationError('File size exceeds maximum limit of 5MB')

def validate_date_range(start_date_field, end_date_field):
    """
    Validate that end date is after start date
    """
    def _validate(form, field):
        start_date = form[start_date_field].data
        end_date = form[end_date_field].data
        
        if start_date and end_date and end_date <= start_date:
            raise ValidationError('End date must be after start date')
    
    return _validate

def validate_required_if(other_field_name, other_field_value):
    """
    Make a field required only if another field has a specific value
    """
    def _validate(form, field):
        other_field = form[other_field_name]
        if other_field.data == other_field_value and not field.data:
            raise ValidationError(f'This field is required when {other_field_name} is {other_field_value}')
    
    return _validate 