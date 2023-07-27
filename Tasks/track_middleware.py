import logging

logger = logging.getLogger(__name__)

class TrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log user's click or activity
        logger.info(f"User {request.user} accessed: {request.path}")

        response = self.get_response(request)
        return response