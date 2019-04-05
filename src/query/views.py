from django.views.generic import TemplateView
from query.servers import solr


class IndexView(TemplateView):
    template_name = 'main/index.html'


class SearchView(TemplateView):
    template_name = 'main/search.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q').split(" ")
        context = self.get_context_data(**kwargs)
        result = solr.get_result(q)
        context['responseHeader'] = result['responseHeader']
        context['results'] = result['response']
        return self.render_to_response(context)
