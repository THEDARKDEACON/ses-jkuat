from flask import Blueprint, request, jsonify
from app import db
from app.models import NewsPost
from flask_login import login_required, current_user

bp = Blueprint('news', __name__)

@bp.route('/api/news', methods=['GET'])
def get_news():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = NewsPost.query.filter_by(is_published=True).order_by(
        NewsPost.created_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    })

@bp.route('/api/news/<int:id>', methods=['GET'])
def get_news_post(id):
    post = NewsPost.query.get_or_404(id)
    return jsonify(post.to_dict())

@bp.route('/api/news', methods=['POST'])
@login_required
def create_news_post():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    post = NewsPost(
        title=data.get('title'),
        content=data.get('content'),
        image_url=data.get('image_url'),
        author_id=current_user.id
    )
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.to_dict()), 201

@bp.route('/api/news/<int:id>', methods=['PUT'])
@login_required
def update_news_post(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    post = NewsPost.query.get_or_404(id)
    data = request.get_json()
    
    if data.get('title'):
        post.title = data['title']
    if data.get('content'):
        post.content = data['content']
    if data.get('image_url'):
        post.image_url = data['image_url']
    if 'is_published' in data:
        post.is_published = data['is_published']
    
    db.session.commit()
    return jsonify(post.to_dict())

@bp.route('/api/news/<int:id>', methods=['DELETE'])
@login_required
def delete_news_post(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    post = NewsPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'News post deleted successfully'}) 