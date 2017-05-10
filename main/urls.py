from django.conf.urls import url
from django.views.generic import TemplateView

from .views import put_message, get_messages

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="main.html")),
    url(r'^put/$', put_message, name="main_put_message"),
    url(r'^get/$', get_messages, name="main_get_messages"),
]
