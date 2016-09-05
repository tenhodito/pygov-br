from pygov_br.base import Client
from xmldict import xml_to_dict


class DeputyClient(Client):

    def __init__(self):
        host = 'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        super(DeputyClient, self).__init__(host)

    def all(self):
        xml_response = self._get('ObterDeputados')
        dict_response = xml_to_dict(xml_response)
        return dict_response['deputados']['deputado']

    def parties(self):
        xml_response = self._get('ObterPartidosCD')
        dict_response = xml_to_dict(xml_response)
        return dict_response['partidos']['partido']

    def deputy_details(self, deputy_id, legislature=''):
        path = 'ObterDetalhesDeputado?ideCadastro={}&numLegislatura={}'
        xml_response = self._get(path.format(deputy_id, legislature))
        dict_response = xml_to_dict(xml_response)
        return dict_response['Deputados']
