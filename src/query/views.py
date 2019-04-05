from math import ceil

from django.views.generic import TemplateView
from query.servers import solr
import re


class IndexView(TemplateView):
    template_name = 'main/index.html'


class SearchView(TemplateView):
    template_name = 'main/search.html'
    paginated_by = 12

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q').replace(":", " ")
        q = re.findall(r"[\w']+", q)
        page = request.GET.get('page')
        try:
            page = int(page) - 1
            page = (0 if page < 1 else page)
        except (ValueError, TypeError):
            page = 0
        context = self.get_context_data(**kwargs)
        result = solr.get_result(q, page * self.paginated_by, self.paginated_by)
        context['responseHeader'] = result['responseHeader']
        context['results'] = result['response']
        context['numPage'] = ceil(context['results']['numFound']/self.paginated_by)
        return self.render_to_response(context)
