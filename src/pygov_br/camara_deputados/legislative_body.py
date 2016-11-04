from pygov_br.base import Client
from datetime import datetime
from xml.etree.ElementTree import fromstring, ElementTree
from xmldict import xml_to_dict


class LegislativeBodyClient(Client):

    def __init__(self):
        host = 'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        super(LegislativeBodyClient, self).__init__(host)

    def all(self):
        """
        List all legislative bodies on Câmara dos Deputados.
        Returns a list of all legislative bodies of Câmara dos Deputados
        (commissions, councils, etc).

        Parameters:
            None
        """
        xml_response = self._get('ObterOrgaos')
        list_response = self._xml_attributes_to_list(xml_response, 'orgao')
        return self._safe(list_response)

    def roles(self):
        """
        List all legislative bodies roles.
        Returns a list of all legislative bodies roles.

        Parameters:
            None
        """
        xml_response = self._get('ListarCargosOrgaosLegislativosCD')
        list_response = self._xml_attributes_to_list(xml_response, 'cargo')
        return self._safe(list_response)

    def members(self, legislative_body_id):
        """
        List all members of a legislative body.
        Returns a list with all members of the legislative body.

        Parameters:
            [Mandatory] legislative_body_id: Integer
        """
        path = 'ObterMembrosOrgao?IDOrgao={}'
        xml_response = self._get(path.format(legislative_body_id))
        element_tree = ElementTree(fromstring(xml_response))
        members = element_tree.find('membros')
        dict_response = self._make_dict_from_tree(members)
        return self._safe(dict_response['membros'])

    def schedule(self, legislative_body_id, initial_date='', final_date=''):
        """
        List all scheduled activities of a legislative body.

        Parameters:
            [Mandatory] legislative_body_id: Integer
            [Optional] initial_date: String (dd/mm/yyyy) or datetime
            [Optional] final_date: String (dd/mm/yyyy) or datetime
        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = "ObterPauta?IDOrgao={}&datIni={}&datFim={}"
        xml_response = self._get(path.format(legislative_body_id,
                                             initial_date, final_date))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['pauta']['reuniao'])

    def types(self):
        """
        List all legislative bodies types.
        Returns a list of all legislative bodies types.

        Parameters:
            None
        """
        xml_response = self._get('ListarTiposOrgaos')
        list_response = self._xml_attributes_to_list(xml_response, 'tipoOrgao')
        return self._safe(list_response)

