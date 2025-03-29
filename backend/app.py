from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NewsPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class GalleryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    events = Event.query.order_by(Event.date.desc()).limit(3).all()
    news = NewsPost.query.order_by(NewsPost.created_at.desc()).limit(3).all()
    return render_template('index.html', events=events, news=news)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/activities')
def activities():
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('activities.html', events=events)

@app.route('/events')
def events():
    # Get filter parameters
    category = request.args.get('category')
    time_filter = request.args.get('time', 'all')  # all, upcoming, past
    sort_by = request.args.get('sort', 'date')  # date, title, category
    sort_order = request.args.get('order', 'desc')  # asc, desc
    
    # Base query
    query = Event.query
    
    # Apply filters
    if category:
        query = query.filter_by(category=category)
    
    if time_filter == 'upcoming':
        query = query.filter(Event.date >= datetime.utcnow())
    elif time_filter == 'past':
        query = query.filter(Event.date < datetime.utcnow())
    
    # Apply sorting
    if sort_by == 'date':
        query = query.order_by(Event.date.desc() if sort_order == 'desc' else Event.date.asc())
    elif sort_by == 'title':
        query = query.order_by(Event.title.desc() if sort_order == 'desc' else Event.title.asc())
    elif sort_by == 'category':
        query = query.order_by(Event.category.desc() if sort_order == 'desc' else Event.category.asc())
    
    # Get categories for filter dropdown
    categories = db.session.query(Event.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    # Execute query
    events = query.all()
    
    return render_template('events.html', 
                         events=events,
                         categories=categories,
                         current_category=category,
                         current_time_filter=time_filter,
                         current_sort=sort_by,
                         current_order=sort_order)

@app.route('/gallery')
def gallery():
    gallery_items = GalleryItem.query.order_by(GalleryItem.created_at.desc()).all()
    return render_template('gallery.html', items=gallery_items)

@app.route('/news')
def news():
    news_posts = NewsPost.query.order_by(NewsPost.created_at.desc()).all()
    return render_template('news.html', news=news_posts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just return a success response
        return jsonify({
            'success': True,
            'message': 'Message sent successfully!'
        })
    
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Username already exists'})
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'})
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful!'})
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # In production, use proper password hashing
            session['user_id'] = user.id
            return jsonify({'success': True, 'message': 'Login successful!'})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/api/events')
def api_events():
    events = Event.query.order_by(Event.date.desc()).all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'date': e.date.isoformat(),
        'image_url': e.image_url
    } for e in events])

@app.route('/api/news')
def api_news():
    posts = NewsPost.query.order_by(NewsPost.created_at.desc()).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'content': p.content,
        'image_url': p.image_url,
        'created_at': p.created_at.isoformat()
    } for p in posts])

@app.route('/events/<int:id>')
def event_detail(id):
    event = Event.query.get_or_404(id)
    return render_template('event_detail.html', event=event)

@app.route('/news/<int:id>')
def news_detail(id):
    post = NewsPost.query.get_or_404(id)
    return render_template('news_detail.html', post=post)

@app.route('/gallery/<int:id>')
def gallery_detail(id):
    item = GalleryItem.query.get_or_404(id)
    return render_template('gallery_detail.html', item=item)

@app.context_processor
def inject_year():
    return {'year': datetime.now().year}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 