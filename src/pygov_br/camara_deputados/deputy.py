from pygov_br.base import Client
from xml.etree.ElementTree import fromstring, ElementTree
from xmldict import xml_to_dict


class DeputyClient(Client):

    def __init__(self):
        host = 'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        super(DeputyClient, self).__init__(host)

    def all(self):
        """
        List all deputies acting on Câmara dos Deputados.

        Parameters:
            None
        Return:
            Returns a list of dictionaries containing the information about
            the deputies.
        """
        xml_response = self._get('ObterDeputados')
        dict_response = xml_to_dict(xml_response)
        return dict_response['deputados']['deputado']

    def details(self, deputy_id, legislature=''):
        """
        List detailed information about a specific deputy.

        Parameters:
            [Mandatory] deputy_id: Integer
            [Optional] lesgislature: Integer
        Return:
            Returns a list of dictionaries containing extra information about
            the deputy. Each dictionary represents one legislative period.

        """
        path = 'ObterDetalhesDeputado?ideCadastro={}&numLegislatura={}'
        xml_response = self._get(path.format(deputy_id, legislature))
        dict_response = xml_to_dict(xml_response)
        return dict_response['Deputados']

    def parties(self):
        """
        List all parties with representation on Câmara dos Deputados.

        Parameters:
            None
        Return:
            Returns a list of dictionaries containing the information about
            the parties.
        """
        xml_response = self._get('ObterPartidosCD')
        dict_response = xml_to_dict(xml_response)
        return dict_response['partidos']['partido']

    def parties_bloc(self, bloc_id='', legislature=''):
        """
        List all parties blocs or filtering by legislature and id.

        Parameters:
            [Optional] bloc_id: Integer
            [Optional] legislature: Integer

        Return:
            Returns a list of dictionaries containing bloc information and a
            list of parties that belongs to the bloc.
        """
        path = 'ObterPartidosBlocoCD?numLegislatura={}&idBloco={}'
        xml_response = self._get(path.format(legislature, bloc_id))
        dict_response = xml_to_dict(xml_response)
        return dict_response['blocos']['bloco']

    def parliamentary_seats(self):
        """
        List all paliamentary seats.

        Parameters:
            None
        Return:
            Returns a list of dictionaries containing the information about
            parliamentaries seats.
        """
        xml_response = self._get('ObterLideresBancadas')
        return self._xml_attributes_to_list(xml_response, 'bancada')

    def parliamentary_seat_leaders(self, seat_initials):
        """
        List all leaders and vice-leaders of a specific paliamentary seat.

        Parameters:
            [Mandatory] seat_initials: String
        Return:
            Returns a dictionary with two keys: 'lider' and 'vice_lider', where
            'lider' is a dictionary and 'vice_lider' a list of dictionaries.
            Both dictionaries contains deputies informations.
        """
        xml_response = self._get('ObterLideresBancadas')
        element_tree = ElementTree(fromstring(xml_response))
        parliamentary_seat = element_tree.find(
            "bancada[@sigla='{}']".format(seat_initials)
        )
        dict_response = self._make_dict_from_tree(parliamentary_seat)
        return dict_response['bancada']
