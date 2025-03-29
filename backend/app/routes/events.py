from flask import Blueprint, request, jsonify
from app import db
from app.models import Event
from flask_login import login_required, current_user
from datetime import datetime

bp = Blueprint('events', __name__)

@bp.route('/api/events', methods=['GET'])
def get_events():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    
    query = Event.query.filter_by(is_published=True)
    if category:
        query = query.filter_by(category=category)
    
    events = query.order_by(Event.date.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'events': [event.to_dict() for event in events.items],
        'total': events.total,
        'pages': events.pages,
        'current_page': events.page
    })

@bp.route('/api/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify(event.to_dict())

@bp.route('/api/events', methods=['POST'])
@login_required
def create_event():
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    event = Event(
        title=data.get('title'),
        description=data.get('description'),
        date=datetime.fromisoformat(data.get('date')),
        location=data.get('location'),
        category=data.get('category'),
        image_url=data.get('image_url'),
        created_by=current_user.id
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify(event.to_dict()), 201

@bp.route('/api/events/<int:id>', methods=['PUT'])
@login_required
def update_event(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    event = Event.query.get_or_404(id)
    data = request.get_json()
    
    if data.get('title'):
        event.title = data['title']
    if data.get('description'):
        event.description = data['description']
    if data.get('date'):
        event.date = datetime.fromisoformat(data['date'])
    if data.get('location'):
        event.location = data['location']
    if data.get('category'):
        event.category = data['category']
    if data.get('image_url'):
        event.image_url = data['image_url']
    if 'is_published' in data:
        event.is_published = data['is_published']
    
    db.session.commit()
    return jsonify(event.to_dict())

@bp.route('/api/events/<int:id>', methods=['DELETE'])
@login_required
def delete_event(id):
    if not current_user.is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted successfully'})

@bp.route('/events/categories', methods=['GET'])
def get_categories():
    categories = db.session.query(Event.category).distinct().all()
    return jsonify([category[0] for category in categories])

@bp.route('/events/upcoming', methods=['GET'])
def get_upcoming_events():
    events = Event.query.filter(
        Event.date >= datetime.utcnow(),
        Event.is_published == True
    ).order_by(Event.date.asc()).all()
    return jsonify([event.to_dict() for event in events])

@bp.route('/events/past', methods=['GET'])
def get_past_events():
    events = Event.query.filter(
        Event.date < datetime.utcnow(),
        Event.is_published == True
    ).order_by(Event.date.desc()).all()
    return jsonify([event.to_dict() for event in events]) 