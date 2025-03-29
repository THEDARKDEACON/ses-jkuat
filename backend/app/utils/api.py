from flask import jsonify, url_for
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)

def unauthorized(message="Unauthorized access"):
    return error_response(401, message)

def forbidden(message="Access forbidden"):
    return error_response(403, message)

def not_found(message="Resource not found"):
    return error_response(404, message)

def server_error(message="Internal server error"):
    return error_response(500, message)

def success_response(data=None, message=None, status_code=200):
    response = {
        'success': True,
        'status_code': status_code
    }
    
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    
    return jsonify(response), status_code

def paginated_response(items, total, page, per_page, endpoint, **kwargs):
    response = {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }
    
    # Add pagination links
    if page > 1:
        response['prev_page'] = url_for(endpoint, page=page-1, per_page=per_page, _external=True, **kwargs)
    if page < response['total_pages']:
        response['next_page'] = url_for(endpoint, page=page+1, per_page=per_page, _external=True, **kwargs)
    
    return success_response(response) 