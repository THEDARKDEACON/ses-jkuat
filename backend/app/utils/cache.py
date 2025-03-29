from functools import wraps
from flask import request, current_app
from datetime import datetime, timedelta
import hashlib
import json

class Cache:
    def __init__(self):
        self._cache = {}
        self._timeouts = {}

    def get(self, key):
        if key in self._cache:
            if key in self._timeouts:
                if datetime.now() > self._timeouts[key]:
                    self.delete(key)
                    return None
            return self._cache[key]
        return None

    def set(self, key, value, timeout=None):
        self._cache[key] = value
        if timeout:
            self._timeouts[key] = datetime.now() + timedelta(seconds=timeout)

    def delete(self, key):
        self._cache.pop(key, None)
        self._timeouts.pop(key, None)

    def clear(self):
        self._cache.clear()
        self._timeouts.clear()

# Initialize cache
cache = Cache()

def cached(timeout=300):
    """
    Cache decorator for view functions
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create a cache key from the function name, args, kwargs, and request data
            key_parts = [
                f.__name__,
                str(args),
                str(sorted(kwargs.items())),
                request.path,
                request.query_string.decode('utf-8')
            ]
            
            if request.is_json:
                key_parts.append(json.dumps(request.get_json(), sort_keys=True))
            
            cache_key = hashlib.md5(''.join(key_parts).encode('utf-8')).hexdigest()
            
            # Try to get the cached response
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # If not cached, call the original function
            response = f(*args, **kwargs)
            
            # Cache the response
            cache.set(cache_key, response, timeout)
            
            return response
        return decorated_function
    return decorator

def cache_key_with_prefix(prefix, *args):
    """
    Generate a cache key with a prefix and arguments
    """
    key_parts = [prefix] + [str(arg) for arg in args]
    return hashlib.md5(''.join(key_parts).encode('utf-8')).hexdigest()

def invalidate_cache_prefix(prefix):
    """
    Invalidate all cache entries with a given prefix
    """
    keys_to_delete = [
        key for key in cache._cache.keys()
        if key.startswith(prefix)
    ]
    for key in keys_to_delete:
        cache.delete(key)

def memoize(timeout=300):
    """
    Memoization decorator for functions with cache timeout
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create a cache key from the function name and arguments
            key_parts = [
                f.__name__,
                str(args),
                str(sorted(kwargs.items()))
            ]
            cache_key = hashlib.md5(''.join(key_parts).encode('utf-8')).hexdigest()
            
            # Try to get the cached result
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # If not cached, call the original function
            result = f(*args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, timeout)
            
            return result
        return decorated_function
    return decorator 