from decouple import config
import requests

CORE_1 = config('CORE_1', cast=str)


class Server:
    server_schema = None
    server_host = None
    server_port = None
    server_path = None

    def __init__(self, server_schema='http', sever_host='127.0.0.1', server_port='8983', server_path=None):
        self.server_schema = server_schema
        self.server_host = sever_host
        self.server_port = server_port
        self.server_path = server_path


class SolrServer(Server):
    core = None

    def __init__(self, core, server_schema='http', server_host='127.0.0.1', server_port='8983', server_path=None):
        super().__init__(server_schema, server_host, server_port, server_path)
        self.core = core

    def get_url(self):
        return "{0}://{1}:{2}/solr/{3}/select".format(self.server_schema, self.server_host, self.server_port, self.core)

    def get_result(self, word, start=0, rows=10):
        query = {'q': ('(title:"{0}"^2 OR content:"{1}"^1)'.format(word, word)), 'indent': 'off', 'wt': 'json',
                 'rows': str(rows),
                 'start': str(start)}
        response = requests.post(self.get_url(), query)
        return response.json()


solr = SolrServer(core='nutch_wofilter', server_host='10.6.0.130')
solr1 = SolrServer(core='scrapy_filter', server_host='10.6.0.130')
