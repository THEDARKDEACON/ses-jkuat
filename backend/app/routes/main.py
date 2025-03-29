from flask import Blueprint, render_template, jsonify
from app.models import Event, NewsPost, GalleryItem
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    events = Event.query.filter_by(is_published=True).order_by(Event.date.desc()).limit(3).all()
    news = NewsPost.query.filter_by(is_published=True).order_by(NewsPost.created_at.desc()).limit(3).all()
    return render_template('index.html', events=events, news=news, now=datetime.now())

@bp.route('/about')
def about():
    return render_template('about.html', now=datetime.now())

@bp.route('/contact')
def contact():
    return render_template('contact.html', now=datetime.now())

@bp.route('/services')
def services():
    return render_template('services.html', now=datetime.now())

@bp.route('/portfolio')
def portfolio():
    gallery_items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    return render_template('portfolio.html', gallery_items=gallery_items, now=datetime.now())

@bp.route('/news')
def news():
    posts = NewsPost.query.filter_by(is_published=True).order_by(NewsPost.created_at.desc()).all()
    return render_template('news.html', posts=posts, now=datetime.now())

# Context processor to make certain variables available to all templates
@bp.app_context_processor
def inject_now():
    return {'now': datetime.now()} 