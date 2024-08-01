from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 400:
            # Customize the response data
            response.data = {
                'details': response.data
            }

    return response
