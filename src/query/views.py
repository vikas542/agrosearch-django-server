from math import ceil

from django.views.generic import TemplateView
from query.servers import solr
import re


class IndexView(TemplateView):
    template_name = 'main/index.html'


class SearchView(TemplateView):
    template_name = 'main/search.html'
    paginated_by = 6

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        page = request.GET.get('page')
        try:
            q = re.findall(r"[\w']+", query.replace(":", " "))
        except AttributeError:
            q = []
        try:
            page = int(page)
            page = (1 if page < 1 else page)
        except (ValueError, TypeError):
            page = 1
        context = self.get_context_data(**kwargs)
        result = solr.get_result(q, (page - 1) * self.paginated_by, self.paginated_by)
        context['responseHeader'] = result['responseHeader']
        context['results'] = result['response']
        context['numPage'] = ceil(context['results']['numFound'] / self.paginated_by)
        context['query'] = query
        context['currentPage'] = page
        return self.render_to_response(context)
