from pygov_br.base import Client
from xmldict import xml_to_dict
from xml.etree.ElementTree import fromstring, ElementTree


class ProposalClient(Client):

    def __init__(self):
        host = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        super(ProposalClient, self).__init__(host)

    def get_by_id(self, proposal_id):
        path = 'ObterProposicaoPorID?IdProp={}'
        xml_response = self._get(path.format(proposal_id))
        element_tree = ElementTree(fromstring(xml_response))
        proposal = element_tree.getroot()

        dict_response = xml_to_dict(fromstring(xml_response), strict=False)
        dict_response = dict_response['proposicao']
        dict_response['tipo'] = proposal.get('tipo')
        dict_response['ano'] = proposal.get('ano')
        dict_response['numero'] = proposal.get('numero')
        return dict_response
