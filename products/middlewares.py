from django.http import HttpRequest
from django.shortcuts import redirect,reverse
from django.contrib import messages
urls = [
    ''
]

class test:
    def __init__(self,get_response):
        self.get_response = get_response
    def __call__(self, request: HttpRequest):
        if  not request.user.is_authenticated and request.path not in urls:
            messages.error(request,'','')
            return redirect(reverse('login'))
        response = self.get_response(request)
        return response