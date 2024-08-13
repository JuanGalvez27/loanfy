from django.urls import reverse


def view_url(view, keyword_args={}):
    url = "http://testserver" + reverse(view, kwargs=keyword_args)
    return url
