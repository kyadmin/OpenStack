from django.shortcuts import render
from django.http import HttpResponse
import hmac
# Create your views here.

def cs_receive_request(request):
    return HttpResponse('I am a test for nginx...')