from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'


class SearchView(TemplateView):
    template_name = 'main/search.html'

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        context = self.get_context_data(**kwargs)
        context['q'] = q
        return self.render_to_response(context)
