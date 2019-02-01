from django.http import HttpResponse

# Create your views here.

def index(self):
    '''Create a default home message'''
    return HttpResponse('Welcome to The Phoenix Homepage')