from rest_framework import status
from django.http import JsonResponse


def index(self):
    '''Create a default home message'''

    response_message = {
        "status": "success",
        "data":
            {"message": "Welcome to Authors Haven's  API.",
             "Owner": "The Phoenix"}
    }
    return JsonResponse(response_message, status=status.HTTP_200_OK)
