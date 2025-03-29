from flask import Blueprint, request, jsonify
from ..models.blog import BlogPost
from .. import db

bp = Blueprint('blog', __name__)

@bp.route('/blog', methods=['GET'])
def get_blog_posts():
    category = request.args.get('category')
    tag = request.args.get('tag')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = BlogPost.query.filter_by(is_published=True)
    
    if category:
        query = query.filter_by(category=category)
    if tag:
        query = query.filter(BlogPost.tags.like(f'%{tag}%'))
    
    pagination = query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'posts': [post.to_dict() for post in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@bp.route('/blog/<int:post_id>', methods=['GET'])
def get_blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()
    return jsonify(post.to_dict())

@bp.route('/blog/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(BlogPost.category).distinct().all()
    return jsonify([category[0] for category in categories])

@bp.route('/blog/tags', methods=['GET'])
def get_tags():
    tags = set()
    posts = BlogPost.query.filter_by(is_published=True).all()
    for post in posts:
        if post.tags:
            tags.update(post.tags.split(','))
    return jsonify(list(tags))

@bp.route('/blog/featured', methods=['GET'])
def get_featured_posts():
    posts = BlogPost.query.filter_by(
        is_published=True
    ).order_by(
        BlogPost.views.desc()
    ).limit(3).all()
    return jsonify([post.to_dict() for post in posts])

@bp.route('/blog/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return jsonify({'likes': post.likes}) 