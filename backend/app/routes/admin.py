from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from ..models.event import Event
from ..models.blog import BlogPost
from .. import db
from functools import wraps

bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'role' in data:
        user.role = data['role']
    if 'name' in data:
        user.name = data['name']
    
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/events', methods=['POST'])
@admin_required
def create_event():
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data['description'],
        date=data['date'],
        location=data['location'],
        image_url=data.get('image_url'),
        category=data['category'],
        created_by=get_jwt_identity()
    )
    
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201

@bp.route('/events/<int:event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(event, key):
            setattr(event, key, value)
    
    db.session.commit()
    return jsonify(event.to_dict())

@bp.route('/blog', methods=['POST'])
@admin_required
def create_blog_post():
    data = request.get_json()
    post = BlogPost(
        title=data['title'],
        content=data['content'],
        excerpt=data.get('excerpt', ''),
        image_url=data.get('image_url'),
        category=data['category'],
        tags=','.join(data.get('tags', [])),
        author_id=get_jwt_identity()
    )
    
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@bp.route('/blog/<int:post_id>', methods=['PUT'])
@admin_required
def update_blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(post, key):
            setattr(post, key, value)
    
    db.session.commit()
    return jsonify(post.to_dict()) 