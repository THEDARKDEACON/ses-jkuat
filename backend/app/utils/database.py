from app import db
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app

def safe_commit():
    """
    Safely commit changes to the database with error handling
    """
    try:
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return False

def add_to_db(model_instance):
    """
    Add a model instance to the database
    """
    try:
        db.session.add(model_instance)
        return safe_commit()
    except Exception as e:
        current_app.logger.error(f"Error adding to database: {str(e)}")
        return False

def delete_from_db(model_instance):
    """
    Delete a model instance from the database
    """
    try:
        db.session.delete(model_instance)
        return safe_commit()
    except Exception as e:
        current_app.logger.error(f"Error deleting from database: {str(e)}")
        return False

def get_or_create(model, defaults=None, **kwargs):
    """
    Get an instance from the database or create it if it doesn't exist
    """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    
    params = dict((k, v) for k, v in kwargs.items())
    if defaults:
        params.update(defaults)
    
    instance = model(**params)
    try:
        db.session.add(instance)
        safe_commit()
        return instance, True
    except Exception as e:
        current_app.logger.error(f"Error in get_or_create: {str(e)}")
        db.session.rollback()
        return None, False

def bulk_insert(model, items):
    """
    Bulk insert multiple items into the database
    """
    try:
        db.session.bulk_insert_mappings(model, items)
        return safe_commit()
    except Exception as e:
        current_app.logger.error(f"Error in bulk insert: {str(e)}")
        return False

def update_or_create(model, defaults=None, **kwargs):
    """
    Update a database instance or create it if it doesn't exist
    """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        for key, value in defaults.items():
            setattr(instance, key, value)
        try:
            return safe_commit(), False
        except Exception as e:
            current_app.logger.error(f"Error updating instance: {str(e)}")
            return False, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        if defaults:
            params.update(defaults)
        instance = model(**params)
        try:
            db.session.add(instance)
            return safe_commit(), True
        except Exception as e:
            current_app.logger.error(f"Error creating instance: {str(e)}")
            return False, False 