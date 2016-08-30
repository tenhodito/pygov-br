from pygov_br.base import Client
from pygov_br.camara_deputados.proposal import ProposalClient
from xmldict import xml_to_dict
from xml.etree.ElementTree import fromstring, ElementTree


class LegislativeBodyClient(Client):

    def __init__(self):
        host = 'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        super(LegislativeBodyClient, self).__init__(host)

    def all(self):
        xml_response = self._get('ObterOrgaos')
        return self._xml_attributes_to_list(xml_response, 'orgao')

    def types(self):
        xml_response = self._get('ListarTiposOrgaos')
        return self._xml_attributes_to_list(xml_response, 'tipoOrgao')

    def proposal_progress(self, proposal_id):
        proposal_client = ProposalClient()
        proposal = proposal_client.get_by_id(proposal_id)
        path = 'ObterAndamento?sigla={}&numero={}&ano={}&dataIni=&codOrgao='
        xml_response = self._get(path.format(
            proposal['tipo'],
            proposal['numero'],
            proposal['ano'])
        )
        dict_response = xml_to_dict(xml_response, strict=False)
        return dict_response['proposicao']

    def _xml_attributes_to_list(self, xml_string, xml_tag):
        element_list = []
        element_tree = ElementTree(fromstring(xml_string))
        for element in element_tree.findall(xml_tag):
            element_list.append(element.attrib)
        return element_list
