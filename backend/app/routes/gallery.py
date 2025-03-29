from flask import Blueprint, request, jsonify
from app import db
from app.models import GalleryItem
from flask_login import login_required, current_user

bp = Blueprint('gallery', __name__)

@bp.route('/api/gallery', methods=['GET'])
def get_gallery():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category = request.args.get('category')
    
    query = GalleryItem.query
    if category:
        query = query.filter_by(category=category)
    
    items = query.order_by(GalleryItem.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': [item.to_dict() for item in items.items],
        'total': items.total,
        'pages': items.pages,
        'current_page': items.page
    })

@bp.route('/api/gallery/<int:id>', methods=['GET'])
def get_gallery_item(id):
    item = GalleryItem.query.get_or_404(id)
    return jsonify(item.to_dict())

@bp.route('/api/gallery', methods=['POST'])
@login_required
def create_gallery_item():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    item = GalleryItem(
        title=data.get('title'),
        description=data.get('description'),
        image_url=data.get('image_url'),
        category=data.get('category'),
        created_by=current_user.id
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify(item.to_dict()), 201

@bp.route('/api/gallery/<int:id>', methods=['PUT'])
@login_required
def update_gallery_item(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    item = GalleryItem.query.get_or_404(id)
    data = request.get_json()
    
    if data.get('title'):
        item.title = data['title']
    if data.get('description'):
        item.description = data['description']
    if data.get('image_url'):
        item.image_url = data['image_url']
    if data.get('category'):
        item.category = data['category']
    
    db.session.commit()
    return jsonify(item.to_dict())

@bp.route('/api/gallery/<int:id>', methods=['DELETE'])
@login_required
def delete_gallery_item(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    item = GalleryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Gallery item deleted successfully'})

@bp.route('/api/gallery/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(GalleryItem.category).distinct().all()
    return jsonify([category[0] for category in categories if category[0]]) 