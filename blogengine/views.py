from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def hello(request):
    return redirect(reverse('posts_list_url'))
