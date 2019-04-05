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

    def __init__(self, core, server_schema='http', sever_host='127.0.0.1', server_port='8983', server_path=None):
        super().__init__(server_schema, sever_host, server_port, server_path)
        self.core = core

    def generate_url(self, word):
        fq = ""
        q = ""
        for w in word:
            fq += "fq=content:%s&" % w
            q += "q=title:%s&" % w

        return self.server_schema + '://' + self.server_host + ':' + self.server_port + '/solr/' + self.core \
               + '/select?' + fq + '&' + q + '&indent=off&wt=json.wrf&rows=100'

    def get_result(self, query):
        response = requests.get(self.generate_url(query))
        return response.json()


solr = SolrServer(core=CORE_1)
