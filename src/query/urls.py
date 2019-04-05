from django.conf.urls import url
from query.views import IndexView, SearchView

app_name = 'main'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^search/$', SearchView.as_view(), name='search')
]
