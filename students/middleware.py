from django.core.cache import cache
from django.http import JsonResponse
import time
import logging
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 10
        self.period = 60

    def __call__(self, request):
        ip = self.get_client_ip(request)
        cache_key = f"rl:{ip}"
        data = cache.get(cache_key, {"count": 0, "timestamp": time.time()})

        elapsed = time.time() - data["timestamp"]
        if elapsed > self.period:
            data = {"count": 1, "timestamp": time.time()}
        else:
            if data["count"] >= self.rate_limit:
                return JsonResponse(
                    {"error": "Too many requests, try again later."},
                    status=429
                )
            data["count"] += 1

        cache.set(cache_key, data, timeout=self.period)
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')




logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        logger.info(f"{request.method} {request.path} completed in {duration:.2f}s")
        return response
