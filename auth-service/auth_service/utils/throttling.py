from typing import Any
from typing import Callable
from functools import wraps

from django.core.cache import cache
from rest_framework.response import Response


def throttle_request(requests_limit: int, time_limit: int) -> Callable:
    def decorator(func) -> Callable:
        @wraps(func)
        def wrapper(self, request, *args, **kwargs) -> Any:
            if request.user.is_authenticated:
                user_id = request.user.id
                key = f"throttle-{user_id}"
                requests_count = cache.get(key, 0)
                if requests_count >= requests_limit:
                    return Response(
                        {"detail": "Too many requests"},
                        status=429,
                    )
                else:
                    cache.set(key, requests_count + 1, time_limit)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
