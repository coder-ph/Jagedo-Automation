import json
import pickle
import hashlib
import functools
from datetime import timedelta
from flask import current_app
import redis

class Cache:
    """A simple Redis-based cache implementation."""
    
    def __init__(self, redis_client, prefix='cache:'):
        """
        Initialize the cache.
        
        Args:
            redis_client: A Redis client instance
            prefix: Prefix for all cache keys
        """
        self.redis = redis_client
        self.prefix = prefix
    
    def _make_key(self, key):
        """Create a cache key with the configured prefix."""
        if not isinstance(key, str):
            key = json.dumps(key, sort_keys=True)
        return f"{self.prefix}{key}"
    
    def get(self, key, default=None):
        """
        Get a value from the cache.
        
        Args:
            key: The cache key
            default: Default value if key not found
            
        Returns:
            The cached value or default if not found
        """
        if not self.redis:
            return default
            
        key = self._make_key(key)
        value = self.redis.get(key)
        
        if value is None:
            return default
            
        try:
            return pickle.loads(value)
        except (pickle.PickleError, TypeError):
            # If unpickling fails, try to return as JSON
            try:
                return json.loads(value)
            except (ValueError, TypeError):
                return default
    
    def set(self, key, value, timeout=None):
        """
        Set a value in the cache.
        
        Args:
            key: The cache key
            value: The value to cache (must be JSON-serializable or picklable)
            timeout: Timeout in seconds (default: None for no timeout)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.redis:
            return False
            
        key = self._make_key(key)
        
        try:
            # Try to pickle the value first
            serialized = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
        except (pickle.PickleError, TypeError):
            # Fall back to JSON if pickling fails
            try:
                serialized = json.dumps(value).encode('utf-8')
            except (TypeError, ValueError):
                current_app.logger.error(f'Failed to serialize value for cache key: {key}')
                return False
        
        try:
            if timeout is not None:
                self.redis.setex(key, int(timeout), serialized)
            else:
                self.redis.set(key, serialized)
            return True
        except Exception as e:
            current_app.logger.error(f'Error setting cache key {key}: {str(e)}')
            return False
    
    def delete(self, *keys):
        """
        Delete one or more keys from the cache.
        
        Args:
            *keys: One or more keys to delete
            
        Returns:
            int: Number of keys deleted
        """
        if not self.redis:
            return 0
            
        keys = [self._make_key(k) for k in keys]
        return self.redis.delete(*keys)
    
    def clear(self, pattern='*'):
        """
        Clear all keys matching the given pattern.
        
        Args:
            pattern: Pattern to match keys against (default: '*')
            
        Returns:
            int: Number of keys deleted
        """
        if not self.redis:
            return 0
            
        pattern = self._make_key(pattern)
        keys = self.redis.keys(pattern)
        
        if keys:
            return self.redis.delete(*keys)
        return 0
    
    def get_or_set(self, key, default=None, timeout=None):
        """
        Get a value from the cache, or set it if not present.
        
        Args:
            key: The cache key
            default: Default value if key not found (can be a callable)
            timeout: Timeout in seconds (default: None for no timeout)
            
        Returns:
            The cached or default value
        """
        value = self.get(key)
        
        if value is None:
            if callable(default):
                value = default()
            else:
                value = default
                
            if value is not None:
                self.set(key, value, timeout=timeout)
                
        return value
    
    def memoize(self, timeout=None, key_func=None):
        """
        Decorator to cache the result of a function.
        
        Args:
            timeout: Timeout in seconds (default: None for no timeout)
            key_func: Optional function to generate cache key from function arguments
            
        Returns:
            Decorated function with caching
        """
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                # Generate a cache key
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    # Default key generation
                    cache_key = f"{f.__module__}.{f.__name__}:{args}:{kwargs}"
                    
                # Try to get from cache
                cached = self.get(cache_key)
                if cached is not None:
                    return cached
                    
                # Call the function and cache the result
                result = f(*args, **kwargs)
                self.set(cache_key, result, timeout=timeout)
                return result
                
            return wrapper
        return decorator

# Initialize a global cache instance
cache = None

def init_cache(app):
    """Initialize the cache with the Flask application."""
    global cache
    
    if app.config.get('REDIS_URL'):
        try:
            redis_client = redis.Redis.from_url(app.config['REDIS_URL'])
            # Test the connection
            redis_client.ping()
        except (redis.RedisError, ConnectionError) as e:
            app.logger.warning(f'Failed to connect to Redis: {str(e)}. Using in-memory cache.')
            redis_client = None
    else:
        redis_client = None
    
    prefix = app.config.get('CACHE_KEY_PREFIX', 'app:')
    cache = Cache(redis_client, prefix=prefix)
    
    # Make cache available in app context
    app.extensions['cache'] = cache
    
    return cache
