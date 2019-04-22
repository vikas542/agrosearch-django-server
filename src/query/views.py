from math import ceil

from django.views.generic import TemplateView
from query.servers import solr, solr1
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
        context['query'] = query
        context['currentPage'] = page

        result = solr1.get_result(q, 0, 0)
        result1 = solr.get_result(q, 0, 0)
        solr_result = int(result['response']['numFound'])
        result['response']['numFound'] += result1['response']['numFound']
        context['numPage'] = ceil(result['response']['numFound'] / self.paginated_by)
        context['responseHeader'] = result['responseHeader']

        start_point = (page - 1) * self.paginated_by
        end_point = (page - 1) * self.paginated_by + self.paginated_by
        # solr1_result = int(result1['response']['numFound'])

        if end_point <= solr_result:
            res = solr1.get_result(q, start_point, self.paginated_by)
            result['response']['docs'] = res['response']['docs']

        elif start_point < solr_result <= end_point:
            res = solr1.get_result(q, start_point, self.paginated_by)
            doc_num_res = len(res['response']['docs'])
            res1 = solr.get_result(q, 0, self.paginated_by - doc_num_res)
            result['response']['docs'] = res['response']['docs'] + res1['response']['docs']

        elif solr_result < start_point:
            res = solr.get_result(q, start_point - solr_result, self.paginated_by)
            result['response']['docs'] = res['response']['docs']

        context['results'] = result['response']
        return self.render_to_response(context)
