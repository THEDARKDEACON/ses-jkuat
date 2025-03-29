from flask import render_template, jsonify, request

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

def not_found_error(error):
    if wants_json_response():
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    return render_template('errors/404.html'), 404

def internal_error(error):
    if wants_json_response():
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error has occurred'
        }), 500
    return render_template('errors/500.html'), 500

def unauthorized_error(error):
    if wants_json_response():
        return jsonify({
            'error': 'Unauthorized',
            'message': 'You must be logged in to access this resource'
        }), 401
    return render_template('errors/401.html'), 401

def forbidden_error(error):
    if wants_json_response():
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    return render_template('errors/403.html'), 403 