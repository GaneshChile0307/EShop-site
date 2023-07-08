from django.shortcuts import redirect,render
from django.urls import reverse


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        print(request.session.get('customer_id'))
        if  not request.session.get("customer_id") :
            while not (request.path == reverse('login')):
                return redirect(reverse('login'))
        response = get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware   