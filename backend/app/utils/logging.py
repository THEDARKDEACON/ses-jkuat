import logging
from logging.handlers import RotatingFileHandler
import os
from flask import has_request_context, request
from functools import wraps
import time
import traceback

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
        else:
            record.url = None
            record.remote_addr = None
            record.method = None
        
        return super().format(record)

def setup_logging(app):
    """
    Set up logging for the application
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Create formatters
    file_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s - %(method)s %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s [in %(module)s]'
    )
    
    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/ses.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('SES startup')

def log_function_call(f):
    """
    Decorator to log function calls with timing
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = f(*args, **kwargs)
            duration = time.time() - start_time
            
            if has_request_context():
                current_app.logger.info(
                    f'Function {f.__name__} completed in {duration:.2f}s - '
                    f'Args: {args}, Kwargs: {kwargs}'
                )
            
            return result
        
        except Exception as e:
            if has_request_context():
                current_app.logger.error(
                    f'Error in {f.__name__}: {str(e)}\n'
                    f'Args: {args}, Kwargs: {kwargs}\n'
                    f'Traceback: {traceback.format_exc()}'
                )
            raise
    
    return decorated_function

def log_error(error, context=None):
    """
    Log an error with context
    """
    if has_request_context():
        current_app.logger.error(
            f'Error: {str(error)}\n'
            f'Context: {context}\n'
            f'URL: {request.url}\n'
            f'Method: {request.method}\n'
            f'IP: {request.remote_addr}\n'
            f'Traceback: {traceback.format_exc()}'
        )
    else:
        current_app.logger.error(
            f'Error: {str(error)}\n'
            f'Context: {context}\n'
            f'Traceback: {traceback.format_exc()}'
        )

def log_info(message, context=None):
    """
    Log an info message with context
    """
    if context:
        current_app.logger.info(f'{message} - Context: {context}')
    else:
        current_app.logger.info(message)

def log_warning(message, context=None):
    """
    Log a warning message with context
    """
    if context:
        current_app.logger.warning(f'{message} - Context: {context}')
    else:
        current_app.logger.warning(message) 